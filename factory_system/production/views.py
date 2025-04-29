from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ProductionStage
from .forms import ProductionStageForm
from orders.models import Order
from datetime import timedelta, datetime
from django.utils.timezone import now
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# --- Helper function ---
def subtract_working_days(from_date, working_days):
    current_date = from_date
    while working_days > 0:
        current_date -= datetime.timedelta(days=1)
        if current_date.weekday() < 5:  # Monday-Friday
            working_days -= 1
    return current_date


@login_required
def production_detail(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)
    return render(request, 'production/production_detail.html', {'stage': stage})

from .templatetags.dict_extras import get_item  # Import if needed

@login_required
def production_list(request):
    stages = ProductionStage.objects.select_related('order', 'order__customer')
    badge_colors = {}
    for stage in stages:
        badge_colors[stage.id] = {
            'sales': get_badge_color(stage.sales_status),
            'programming': get_badge_color(stage.programming_status),
            'nest': get_badge_color(stage.nest_status),
            'edge': get_badge_color(stage.edge_status),
            'prep': get_badge_color(stage.prep_status),
            'build': get_badge_color(stage.build_status),
            'fittings': get_badge_color(stage.fittings_status),
            'wrapping': get_badge_color(stage.wrapping_status),
            'quality': get_badge_color(stage.quality_status),
        }
    return render(request, 'production/production_list.html', {
        'stages': stages,
        'badge_colors': badge_colors,
        'status_fields': ['sales', 'programming', 'nest', 'edge', 'prep', 'build', 'fittings', 'wrapping', 'quality'],
    })



@login_required
def production_edit(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)
    orders = Order.objects.select_related('customer')  # <-- Add this
    if request.method == 'POST':
        form = ProductionStageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            return redirect('production:production_detail', pk=pk)
    else:
        form = ProductionStageForm(instance=stage)

    return render(request, 'production/production_form.html', {
        'form': form,
        'editing': True,
        'stage': stage,
        'orders': orders,   # <-- Pass orders here too
    })




def production_create(request):
    orders = Order.objects.select_related('customer')
    if request.method == 'POST':
        form = ProductionStageForm(request.POST)
        if form.is_valid():
            production_stage = form.save(commit=False)

            # Calculate target dates based on the delivery date
            if production_stage.order.delivery_date:
                delivery_date = production_stage.order.delivery_date

                # Helper to skip weekends
                def adjust_to_weekday(date):
                    while date.weekday() in (5, 6):  # Saturday = 5, Sunday = 6
                        date -= timedelta(days=1)
                    return date

                production_stage.sales_target_date = adjust_to_weekday(delivery_date - timedelta(days=14))
                production_stage.programming_target_date = adjust_to_weekday(delivery_date - timedelta(days=9))
                production_stage.nest_target_date = adjust_to_weekday(delivery_date - timedelta(days=8))
                production_stage.edge_target_date = adjust_to_weekday(delivery_date - timedelta(days=7))
                production_stage.prep_target_date = adjust_to_weekday(delivery_date - timedelta(days=6))
                production_stage.build_target_date = adjust_to_weekday(delivery_date - timedelta(days=5))
                production_stage.fittings_target_date = adjust_to_weekday(delivery_date - timedelta(days=4))
                production_stage.wrapping_target_date = adjust_to_weekday(delivery_date - timedelta(days=3))
                production_stage.quality_target_date = adjust_to_weekday(delivery_date - timedelta(days=2))

                # Estimate sheets + cabs
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

def get_badge_color(status):
    if status == 'NOT_STARTED':
        return 'secondary'
    elif status == 'IN_PROGRESS':
        return 'warning'
    elif status == 'STUCK':
        return 'danger'
    elif status == 'ON_HOLD':
        return 'dark'
    elif status == 'CONFIRMATION':
        return 'primary'
    elif status == 'COMPLETED':
        return 'success'
    elif status == 'NO_PAPERWORK':
        return 'danger'
    else:
        return 'secondary'

def production_detail(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)

    context = {
        'stage': stage,
        'badge_colors': {
            'sales_status': get_badge_color(stage.sales_status),
            'programming_status': get_badge_color(stage.programming_status),
            'nest_status': get_badge_color(stage.nest_status),
            'edge_status': get_badge_color(stage.edge_status),
            'prep_status': get_badge_color(stage.prep_status),
            'build_status': get_badge_color(stage.build_status),
            'fittings_status': get_badge_color(stage.fittings_status),
            'wrapping_status': get_badge_color(stage.wrapping_status),
            'quality_status': get_badge_color(stage.quality_status),
        }
    }
    return render(request, 'production/production_detail.html', context)

@login_required
def production_delete(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)
    if request.method == 'POST':
        stage.delete()
        return redirect('production:production_list')
    return redirect('production:production_detail', pk=pk)


@csrf_exempt
@login_required
def production_update_status(request, pk):
    if request.method == 'POST':
        try:
            stage = get_object_or_404(ProductionStage, pk=pk)
            data = json.loads(request.body)

            status_field = data.get('status_field')
            new_value = data.get('new_value')

            if status_field and hasattr(stage, status_field):
                setattr(stage, status_field, new_value)
                stage.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid field'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})