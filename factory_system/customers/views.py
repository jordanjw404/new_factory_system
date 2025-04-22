from django.shortcuts import render, redirect
from .forms import CustomerForm

def create_customer_view(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer-list")  # You can change this later
    else:
        form = CustomerForm()

    return render(request, "customers/create_customer.html", {"form": form})
