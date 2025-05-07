from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views import View
from .models import Item, Location, ItemStock, Movement, BoardStock, IncomingOrder, IncomingOrderItem
from .forms import StockInForm, StockOutForm, TransferForm, AddItemForm, BoardStockForm, IncomingOrderForm, IncomingOrderItemFormSet
from django.db import transaction


# View for adding new stock (Stock In)
class StockInView(View):
    def get(self, request):
        form = StockInForm()
        return render(request, 'inventory/stock_in.html', {'form': form})

    def post(self, request):
        form = StockInForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            location = form.cleaned_data['location']
            quantity = form.cleaned_data['quantity']
            reason = form.cleaned_data['reason']

            # Update ItemStock
            stock, created = ItemStock.objects.get_or_create(item=item, location=location)
            stock.quantity += quantity
            stock.save()

            # Create Movement Record
            Movement.objects.create(
                item=item,
                quantity=quantity,
                move_type=Movement.MovementType.IN,
                to_location=location,
                user=request.user,
                reference=reason,
                notes=reason
            )

            messages.success(request, f"Successfully added {quantity} of {item.name} to {location.name}.")
            return redirect(reverse('inventory:item_list'))

        messages.error(request, "Failed to add stock. Please correct the errors below.")
        return render(request, 'inventory/stock_in.html', {'form': form})


# View for removing stock (Stock Out)
class StockOutView(View):
    def get(self, request):
        form = StockOutForm()
        return render(request, 'inventory/stock_out.html', {'form': form})

    def post(self, request):
        form = StockOutForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            location = form.cleaned_data['location']
            quantity = form.cleaned_data['quantity']
            reason = form.cleaned_data['reason']

            # Update ItemStock
            stock = ItemStock.objects.get(item=item, location=location)
            stock.quantity -= quantity
            stock.save()

            # Create Movement Record
            Movement.objects.create(
                item=item,
                quantity=quantity,
                move_type=Movement.MovementType.OUT,
                from_location=location,
                user=request.user,
                reference=reason,
                notes=reason
            )

            messages.success(request, f"Successfully removed {quantity} of {item.name} from {location.name}.")
            return redirect(reverse('inventory:item_list'))

        messages.error(request, "Failed to remove stock. Please correct the errors below.")
        return render(request, 'inventory/stock_out.html', {'form': form})


# View for transferring stock
class TransferView(View):
    def get(self, request):
        form = TransferForm()
        return render(request, 'inventory/transfer.html', {'form': form})

    def post(self, request):
        form = TransferForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            from_location = form.cleaned_data['from_location']
            to_location = form.cleaned_data['to_location']
            quantity = form.cleaned_data['quantity']
            reason = form.cleaned_data['reason']

            # Update ItemStock at source
            from_stock = ItemStock.objects.get(item=item, location=from_location)
            from_stock.quantity -= quantity
            from_stock.save()

            # Update ItemStock at destination
            to_stock, created = ItemStock.objects.get_or_create(item=item, location=to_location)
            to_stock.quantity += quantity
            to_stock.save()

            # Create Movement Record
            Movement.objects.create(
                item=item,
                quantity=quantity,
                move_type=Movement.MovementType.TRANSFER,
                from_location=from_location,
                to_location=to_location,
                user=request.user,
                reference=reason,
                notes=reason
            )

            messages.success(request, f"Successfully transferred {quantity} of {item.name} from {from_location.name} to {to_location.name}.")
            return redirect(reverse('inventory:item_list'))

        messages.error(request, "Failed to transfer stock. Please correct the errors below.")
        return render(request, 'inventory/transfer.html', {'form': form})


# View for adding and editing items
class AddItemView(View):
    def get(self, request):
        form = AddItemForm()
        return render(request, 'inventory/add_item.html', {'form': form})

    def post(self, request):
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item added successfully.")
            return redirect(reverse('inventory:item_list'))

        messages.error(request, "Failed to add item. Please correct the errors below.")
        return render(request, 'inventory/add_item.html', {'form': form})


# View for creating board stock (offcuts)
class BoardStockCreateView(View):
    def get(self, request):
        form = BoardStockForm()
        return render(request, 'inventory/board_stock_form.html', {'form': form})

    def post(self, request):
        form = BoardStockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Board stock added successfully.")
            return redirect(reverse('inventory:board_list'))

        messages.error(request, "Failed to add board stock. Please correct the errors below.")
        return render(request, 'inventory/board_stock_form.html', {'form': form})
