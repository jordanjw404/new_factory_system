from django.shortcuts import render, get_object_or_404
from .models import Order
from django.contrib.auth.decorators import login_required

@login_required
def order_list(request):
    orders = Order.objects.select_related("customer", "owner").order_by("-created_at")
    return render(request, "orders/orders_list.html", {"orders": orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "orders/order_detail.html", {"order": order})