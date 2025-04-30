from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from .models import Item, Location, ItemStock, Movement
from .forms import StockInForm, StockOutForm, TransferForm


@login_required
@permission_required('inventory.add_movement', raise_exception=True)
def stock_in(request):
    form = StockInForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        item = form.cleaned_data['item']
        location = form.cleaned_data['location']
        qty = form.cleaned_data['quantity']
        reason = form.cleaned_data['reason'] or "Stock In"

        with transaction.atomic():
            stock, _ = ItemStock.objects.select_for_update().get_or_create(item=item, location=location, defaults={'quantity': 0})
            stock.quantity += qty
            stock.save()

            Movement.objects.create(
                item=item,
                from_location=None,
                to_location=location,
                quantity=qty,
                move_type="IN",
                user=request.user,
                reason=reason
            )
        messages.success(request, f"Stocked in {qty} of {item.code} to {location.name}.")
        return redirect('stock-in')
    return render(request, 'inventory/stock_in.html', {'form': form})


@login_required
@permission_required('inventory.add_movement', raise_exception=True)
def stock_out(request):
    form = StockOutForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        item = form.cleaned_data['item']
        location = form.cleaned_data['location']
        qty = form.cleaned_data['quantity']
        reason = form.cleaned_data['reason'] or "Stock Out"

        stock = ItemStock.objects.filter(item=item, location=location).first()
        if not stock or stock.quantity < qty:
            messages.error(request, "Insufficient stock at this location.")
        else:
            with transaction.atomic():
                stock = ItemStock.objects.select_for_update().get(item=item, location=location)
                stock.quantity -= qty
                stock.save()

                Movement.objects.create(
                    item=item,
                    from_location=location,
                    to_location=None,
                    quantity=qty,
                    move_type="OUT",
                    user=request.user,
                    reason=reason
                )
            messages.success(request, f"Stocked out {qty} of {item.code} from {location.name}.")
            return redirect('stock-out')
    return render(request, 'inventory/stock_out.html', {'form': form})


@login_required
@permission_required('inventory.add_movement', raise_exception=True)
def stock_transfer(request):
    form = TransferForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        item = form.cleaned_data['item']
        from_location = form.cleaned_data['from_location']
        to_location = form.cleaned_data['to_location']
        qty = form.cleaned_data['quantity']
        reason = form.cleaned_data['reason'] or "Internal Transfer"

        if from_location == to_location:
            messages.error(request, "Source and destination cannot be the same.")
        else:
            stock = ItemStock.objects.filter(item=item, location=from_location).first()
            if not stock or stock.quantity < qty:
                messages.error(request, "Insufficient stock at source location.")
            else:
                with transaction.atomic():
                    from_stock = ItemStock.objects.select_for_update().get(item=item, location=from_location)
                    from_stock.quantity -= qty
                    from_stock.save()

                    to_stock, _ = ItemStock.objects.select_for_update().get_or_create(item=item, location=to_location, defaults={'quantity': 0})
                    to_stock.quantity += qty
                    to_stock.save()

                    Movement.objects.create(
                        item=item,
                        from_location=from_location,
                        to_location=to_location,
                        quantity=qty,
                        move_type="TRANSFER",
                        user=request.user,
                        reason=reason
                    )
                messages.success(request, f"Transferred {qty} of {item.code} from {from_location.name} to {to_location.name}.")
                return redirect('stock-transfer')
    return render(request, 'inventory/transfer.html', {'form': form})
