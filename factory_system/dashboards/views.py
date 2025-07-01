from django.shortcuts import render
from django.db.models import Sum, Count
from production.models import ProductionStage  # Correct import for ProductionStage
from orders.models import Order  # Correct import for Order
from customers.models import Customer  # Correct import for Customer

# KPI Functions
def total_cabs_in_production():
    total_cabs = ProductionStage.objects.aggregate(total_cabs=Sum('estimated_build_cabs'))['total_cabs'] or 0
    return total_cabs

def orders_by_status():
    orders_status = Order.objects.values('status').annotate(order_count=Count('id')).order_by('status')
    return orders_status

def customer_overview():
    customer_data = Customer.objects.annotate(order_count=Count('orders'))
    return customer_data

# Dashboard View
def factory_kpi_dashboard(request):
    # Get the KPIs
    total_cabs = total_cabs_in_production()
    orders_by_status_data = orders_by_status()
    customer_data = customer_overview()

    # Render the dashboard with the data
    return render(request, 'dashboards/kpi_dashboard.html', {
        'total_cabs': total_cabs,
        'orders_by_status': orders_by_status_data,
        'customer_data': customer_data,
    })
