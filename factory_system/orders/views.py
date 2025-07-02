from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .filters import OrderFilter
import csv, openpyxl
from django.http import HttpResponse
from django.contrib import messages
from .forms import OrderForm, DeliveryDateUpdateForm
from production.utils import create_production_stage, compute_stage_targets

@login_required
def order_list(request):
    order_by = request.GET.get("sort", "-created_at")
    order_filter = OrderFilter(request.GET, queryset=Order.objects.select_related("customer", "owner").order_by(order_by))

    return render(request, "orders/orders_list.html", {
        "filter": order_filter,
        "orders": order_filter.qs,
        "current_sort": order_by,
    })


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "orders/orders_detail.html", {"order": order})

@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            
            # Create production stage if needed
            if order.send_to_production:
                from production.utils import create_production_stage
                create_production_stage(order)
                
            return redirect("orders:order_list")
    else:
        form = OrderForm()
    return render(request, "orders/order_form.html", {"form": form})


@login_required
def order_detail_list(request):
    order_filter = OrderFilter(request.GET, queryset=Order.objects.select_related("customer", "owner").order_by("-created_at"))
    return render(request, "orders/orders_detail_list.html", {
        "filter": order_filter,
        "orders": order_filter.qs
    })

@login_required
def export_orders_excel(request):
    order_filter = OrderFilter(request.GET, queryset=Order.objects.select_related("customer", "owner"))
    orders = order_filter.qs

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Orders"

    headers = ["ID", "Customer", "Ref", "Type", "Status", "Delivery Date", "Owner"]
    worksheet.append(headers)

    for order in orders:
        worksheet.append([
            order.id,
            order.customer.name,
            order.reference,
            order.get_order_type_display(),
            order.get_status_display(),
            order.delivery_date.strftime("%Y-%m-%d") if order.delivery_date else "",
            str(order.owner),
        ])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = "attachment; filename=orders_export.xlsx"
    workbook.save(response)
    return response

@login_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    original_delivery_date = order.delivery_date
    
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            new_delivery = form.cleaned_data['delivery_date']
            
            # Check if delivery date changed
            if original_delivery_date != new_delivery:
                # Save order without updating production dates
                order = form.save()
                
                # Store original date in session for confirmation view
                request.session['original_delivery_date'] = original_delivery_date.isoformat()
                return redirect('orders:delivery_date_update', pk=order.pk)
            
            # No date change - save normally
            order = form.save()
            messages.success(request, "Order updated successfully")
            return redirect('orders:order_list')
    else:
        form = OrderForm(instance=order)
    
    return render(request, 'orders/order_form.html', {
        "form": form, 
        "edit_mode": True,
        "order": order
    })



@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order_name = order.name
        order_id = order.id
        order.delete()
        messages.success(request, f"Order #{order_id} ({order_name}) deleted successfully.")
        return redirect('orders:order_list')
    return render(request, 'orders/order_confirm_delete.html', {"order": order})

@login_required
def delivery_date_update(request, pk):
    """Confirmation view for delivery date changes"""
    order = get_object_or_404(Order, pk=pk)
    original_date = request.session.pop('original_delivery_date', None)
    
    if not original_date:
        messages.warning(request, "Session expired. Please update the order again.")
        return redirect('orders:order_edit', pk=pk)
    
    try:
        original_date = date.fromisoformat(original_date)
    except (TypeError, ValueError):
        messages.error(request, "Invalid date format")
        return redirect('orders:order_edit', pk=pk)
    
    if request.method == "POST":
        form = DeliveryDateUpdateForm(request.POST)
        if form.is_valid():
            update_choice = form.cleaned_data['update_choice']
            
            if update_choice == 'all':
                # Recalculate all production dates
                if hasattr(order, 'productionstage'):
                    # Calculate new targets
                    targets = compute_stage_targets(order.delivery_date)
                    
                    # Update only target dates
                    for stage, target_date in targets.items():
                        setattr(
                            order.productionstage, 
                            f"{stage}_target_date", 
                            target_date
                        )
                    order.productionstage.save()
                    messages.success(request, "All production dates updated")
                else:
                    messages.info(request, "No production stage to update")
            
            messages.success(request, "Order updated successfully")
            return redirect('orders:order_list')
    else:
        form = DeliveryDateUpdateForm()
    
    return render(request, 'orders/delivery_date_update.html', {
        'form': form,
        'order': order,
        'original_date': original_date,
        'new_date': order.delivery_date,
    })