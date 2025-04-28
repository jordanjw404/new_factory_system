from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ProductionStage
from .forms import ProductionStageForm
from orders.models import Order
from datetime import timedelta
from django.utils.timezone import now

# --- Helper function ---
def subtract_working_days(from_date, working_days):
    current_date = from_date
    while working_days > 0:
        current_date -= datetime.timedelta(days=1)
        if current_date.weekday() < 5:  # Monday-Friday
            working_days -= 1
    return current_date

# --- Production List View ---
@login_required
def production_list(request):
    stages = ProductionStage.objects.select_related('order', 'order__customer')
    return render(request, 'production/production_list.html', {
        'stages': stages,
    })



@login_required
def production_create(request):
    orders = Order.objects.select_related('customer')
    if request.method == 'POST':
        form = ProductionStageForm(request.POST)
        if form.is_valid():
            production_stage = form.save(commit=False)

            # Fetch delivery date
            delivery_date = production_stage.order.delivery_date

            # Calculate each stage
            def workday_before(date, days_back):
                new_date = date
                while days_back > 0:
                    new_date -= timedelta(days=1)
                    if new_date.weekday() < 5:  # Monday = 0, Sunday = 6
                        days_back -= 1
                return new_date

            # Set target dates
            production_stage.sales_target_date = workday_before(delivery_date, 14)
            production_stage.programming_target_date = workday_before(delivery_date, 8)
            production_stage.nest_target_date = workday_before(delivery_date, 7)
            production_stage.edge_target_date = workday_before(delivery_date, 6)
            production_stage.prep_target_date = workday_before(delivery_date, 5)
            production_stage.build_target_date = workday_before(delivery_date, 4)
            production_stage.fittings_target_date = workday_before(delivery_date, 3)
            production_stage.wrapping_target_date = workday_before(delivery_date, 2)
            production_stage.quality_target_date = workday_before(delivery_date, 1)

            # Auto-calculate sheets and cabs too
            production_stage.estimated_nest_sheets = (
                production_stage.order.cabs * 0.55 +
                production_stage.order.robes * 0.86 +
                production_stage.order.panels * 0.1
            )
            production_stage.estimated_build_cabs = (
                production_stage.order.cabs + production_stage.order.robes
            )

            production_stage.save()
            return redirect('production:production_list')
    else:
        form = ProductionStageForm()

    return render(request, 'production/production_form.html', {'form': form, 'orders': orders})

@login_required
def production_detail(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)
    return render(request, 'production/production_detail.html', {'stage': stage})