from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .filters import OrderFilter
import csv, openpyxl
from django.http import HttpResponse


@login_required
def order_list(request):
    order_filter = OrderFilter(request.GET, queryset=Order.objects.select_related("customer", "owner").order_by("-created_at"))
    return render(request, "orders/orders_list.html", {
        "filter": order_filter,
        "orders": order_filter.qs,
    })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "orders/order_detail.html", {"order": order})

@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
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