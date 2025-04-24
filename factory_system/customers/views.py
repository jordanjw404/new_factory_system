from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm
from .models import Customer
from .filters import CustomerFilter
from django.contrib import messages
@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            return redirect('customers:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form})

@login_required
def customer_list(request):
    customer_filter = CustomerFilter(request.GET, queryset=Customer.objects.all())
    return render(request, 'customers/customer_list.html', {
        'filter': customer_filter,
        'customers': customer_filter.qs,
    })

@login_required
def customer_detail_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_detail_list.html', {'customers': customers})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customers/customer_detail.html', {'customer': customer})

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated successfully.")
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/customer_form.html', {'form': form, 'edit_mode': True})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        customer.delete()
        messages.success(request, "Customer deleted successfully.")
        return redirect('customers:customer_list')

    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})
