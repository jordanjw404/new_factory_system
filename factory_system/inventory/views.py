from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models import Count, Sum
from .models import Item, Location, ItemStock, Movement, BoardStock
from .forms import StockInForm, StockOutForm, TransferForm,IncomingOrderForm, IncomingOrderItemFormSet, BoardStockForm, AddItemForm
from .models import IncomingOrder
import csv
from django.http import HttpResponse



@login_required
@permission_required('inventory.add_movement', raise_exception=True)
def stock_in(request):
    form = StockInForm(request.POST or None)

    # Pre-fill item if ?item_id is present
    item_id = request.GET.get('item_id')
    if item_id and not form.is_bound:
        form.fields['item'].initial = Item.objects.filter(id=item_id).first()

    if request.method == 'POST' and form.is_valid():
        item = form.cleaned_data['item']
        location = form.cleaned_data['location']
        qty = form.cleaned_data['quantity']
        reason = form.cleaned_data['reason'] or "Stock In"

        with transaction.atomic():
            stock, _ = ItemStock.objects.select_for_update().get_or_create(
                item=item, location=location, defaults={'quantity': 0}
            )
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

    item_id = request.GET.get('item_id')
    if item_id and not form.is_bound:
        form.fields['item'].initial = Item.objects.filter(id=item_id).first()

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

    item_id = request.GET.get('item_id')
    if item_id and not form.is_bound:
        form.fields['item'].initial = Item.objects.filter(id=item_id).first()

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

                    to_stock, _ = ItemStock.objects.select_for_update().get_or_create(
                        item=item, location=to_location, defaults={'quantity': 0}
                    )
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
                messages.success(
                    request,
                    f"Transferred {qty} of {item.code} from {from_location.name} to {to_location.name}."
                )
                return redirect('stock-transfer')

    return render(request, 'inventory/transfer.html', {'form': form})


def inventory_list(request):
    items = Item.objects.annotate(
        total_quantity=Sum('stock_levels__quantity')
    ).order_by('type', 'code')
    return render(request, 'inventory/inventory_list.html', {'items': items})


def inventory_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    stock_by_location = item.stock_levels.select_related('location').order_by('location__name')
    recent_movements = Movement.objects.filter(item=item).select_related('user').order_by('-timestamp')[:10]
    return render(request, 'inventory/inventory_detail.html', {
        'item': item,
        'stock_by_location': stock_by_location,
        'recent_movements': recent_movements,
    })

@login_required
def movement_log(request):
    movements = Movement.objects.select_related('item', 'from_location', 'to_location', 'user')

    # Optional filters
    item_id = request.GET.get("item")
    user_id = request.GET.get("user")
    move_type = request.GET.get("type")

    if item_id:
        movements = movements.filter(item__id=item_id)
    if user_id:
        movements = movements.filter(user__id=user_id)
    if move_type:
        movements = movements.filter(move_type=move_type)

    movements = movements.order_by('-timestamp')[:200]  # Limit for performance

    return render(request, 'inventory/movement_log.html', {
        'movements': movements,
    })



@login_required
def create_incoming_order(request):
    if request.method == 'POST':
        form = IncomingOrderForm(request.POST)
        formset = IncomingOrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            formset.instance = order
            formset.save()
            messages.success(request, "Incoming order created.")
            return redirect('incoming-order-list')  # You'll create this view later
    else:
        form = IncomingOrderForm()
        formset = IncomingOrderItemFormSet()
    return render(request, 'inventory/incoming_order_form.html', {
        'form': form,
        'formset': formset
    })

@login_required
def incoming_order_list(request):
    orders = IncomingOrder.objects.select_related('supplier', 'created_by').order_by('-expected_date')
    return render(request, 'inventory/incoming_order_list.html', {'orders': orders})


@login_required
def incoming_order_detail(request, pk):
    order = get_object_or_404(IncomingOrder.objects.select_related('supplier', 'created_by'), pk=pk)
    items = order.items.select_related('item', 'location')
    return render(request, 'inventory/incoming_order_detail.html', {'order': order, 'items': items})



@login_required
def export_inventory_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Code', 'Name', 'Type', 'Quantity', 'Unit'])

    items = Item.objects.all()
    for item in items:
        writer.writerow([item.id, item.code, item.name, item.get_type_display(), item.total_quantity or 0, item.unit])

    return response

@login_required
def add_stock_item(request):
    return render(request, 'inventory/add_item_form.html')


def import_inventory(request):
    return HttpResponse("Import view coming soon.")

def export_inventory(request):
    return HttpResponse("Import view coming soon.")



@login_required
@permission_required('inventory.add_item', raise_exception=True)
def add_stock_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f"Item '{item.code}' added successfully.")
            return redirect('inventory-list')
    else:
        form = AddItemForm()

    return render(request, 'inventory/add_stock_item.html', {'form': form})



def boardstock_list(request):
    pieces = BoardStock.objects.select_related('parent_board', 'location', 'allocated_to')
    return render(request, 'inventory/boardstock_list.html', {'pieces': pieces})


def boardstock_create(request):
    if request.method == 'POST':
        form = BoardStockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Board stock added successfully.")
            return redirect('board-stock-list')
    else:
        form = BoardStockForm()
    return render(request, 'inventory/add_board_stock.html', {'form': form})
