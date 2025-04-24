from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm
from .models import Customer
from . import views

@login_required
def create_customer_view(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        customer = form.save(commit=False)
        customer.created_by = request.user
        customer.save()
        return redirect("dashboard")  # or a customer list later
    return render(request, "customers/create_customer.html", {"form": form})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customers/customer_detail.html', {'customer': customer})
