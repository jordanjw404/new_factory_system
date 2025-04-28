from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ProductionStage
from .filters import ProductionStageFilter
from .forms import ProductionStageForm
from orders.models import Order

@login_required
def production_list(request):
    production_filter = ProductionStageFilter(request.GET, queryset=ProductionStage.objects.select_related('order', 'order__customer'))
    return render(request, 'production/production_list.html', {
        'filter': production_filter,
        'stages': production_filter.qs,
    })

@login_required
def production_detail(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)
    return render(request, 'production/production_detail.html', {'stage': stage})

@login_required
def production_create(request):
    orders = Order.objects.select_related('customer')  # <-- Load all orders at the top

    if request.method == 'POST':
        form = ProductionStageForm(request.POST)
        if form.is_valid():
            production_stage = form.save(commit=False)

            # Auto-calculate estimation based on selected order
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
