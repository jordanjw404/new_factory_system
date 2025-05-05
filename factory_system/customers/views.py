from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm , CustomerImportForm
from .models import Customer
from .filters import CustomerFilter
from django.contrib import messages
import csv, io


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

from django.db.models import Count

from django.db.models import Count

@login_required
def customer_list(request):
    # Annotate first
    queryset = Customer.objects.annotate(order_count=Count('orders'))

    # Then apply status filter
    status = request.GET.get('status')
    if status == 'active':
        queryset = queryset.filter(is_active=True)
    elif status == 'inactive':
        queryset = queryset.filter(is_active=False)

    # Apply your name filter
    customer_filter = CustomerFilter(request.GET, queryset=queryset)

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

import csv
from django.http import HttpResponse
from .models import Customer

@login_required
def export_customers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Name', 'Contact Name', 'Email', 'Phone', 'Mobile',
        'Address 1', 'Address 2', 'City', 'Post Code',
        'Notes', 'Is Active', 'Created At', 'Updated At', 'Created By'
    ])

    for customer in Customer.objects.all():
        writer.writerow([
            customer.id,
            customer.name,
            customer.contact_name,
            customer.email,
            customer.phone,
            customer.mobile,
            customer.address_1,
            customer.address_2,
            customer.city,
            customer.postcode,
            customer.notes,
            "Yes" if customer.is_active else "No",
            customer.created_at.strftime('%Y-%m-%d %H:%M'),
            customer.updated_at.strftime('%Y-%m-%d %H:%M'),
            customer.created_by.username if customer.created_by else 'N/A',
        ])

    return response

@login_required
def import_customers_csv(request):
    if request.method == 'POST':
        form = CustomerImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            data = csv_file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(data))

            count = 0
            for row in reader:
                Customer.objects.create(
                    name=row['Name'],
                    contact_name=row.get('Contact Name', ''),
                    email=row.get('Email', ''),
                    phone=row.get('Phone', ''),
                    mobile=row.get('Mobile', ''),
                    address_1=row.get('Address 1', ''),
                    address_2=row.get('Address 2', ''),
                    city=row.get('City', ''),
                    post_code=row.get('Post Code', ''),
                    notes=row.get('Notes', ''),
                    is_active=(row.get('Is Active', '').lower() == 'yes'),
                    created_by=request.user
                )
                count += 1

            messages.success(request, f"{count} customers imported successfully.")
            return redirect('customers:customer_list')
    else:
        form = CustomerImportForm()

    return render(request, 'customers/import_customers.html', {'form': form})