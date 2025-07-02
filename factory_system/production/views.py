# production/views.py

import csv
import json
from datetime import datetime
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import pandas as pd

from .models import ProductionStage
from .forms import ProductionStageForm
from .filters import ProductionStageFilter
from .utils import create_production_stage,update_stage_status
from orders.models import Order

STATUS_FIELDS = [
    'sales','programming','nest','edge',
    'prep','build','fittings','wrapping','quality'
]

def get_badge_color(status):
    return {
        'NOT_STARTED': 'secondary',
        'IN_PROGRESS': 'warning',
        'STUCK': 'danger',
        'ON_HOLD': 'dark',
        'COMPLETED': 'success',
        'READY': 'info',
        'CONFIRMATION': 'primary',
        'NO_PAPERWORK': 'danger',
    }.get(status, 'secondary')

@login_required
def production_list(request):
    stages = ProductionStage.objects.select_related('order','order__customer')
    badge_colors = {
        st.id: {
            f: get_badge_color(getattr(st, f"{f}_status"))
            for f in STATUS_FIELDS
        } for st in stages
    }
    return render(request, 'production/production_list.html', {
        'stages': stages,
        'badge_colors': badge_colors,
        'status_fields': STATUS_FIELDS,
    })

@login_required
def production_detail(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)
    badge_colors = {
        f: get_badge_color(getattr(stage, f"{f}_status"))
        for f in STATUS_FIELDS
    }
    return render(request, 'production/production_detail.html', {
        'stage': stage,
        'badge_colors': badge_colors,
    })

@login_required
def production_create(request, order_pk=None):
    """
    If called via POST with an order_pk, this will create (or refresh)
    the ProductionStage for that order, computing all target dates.
    """
    # You can either pass order_pk via URL, or choose from a form.
    if request.method == 'POST' and order_pk:
        order = get_object_or_404(Order, pk=order_pk)
        stage = create_production_stage(order)
        return redirect('production:production_detail', pk=stage.pk)

    # Otherwise show a simple chooser of Orders without a stage yet
    # (optional — adapt to your needs)
    orders = Order.objects.filter(productionstage__isnull=True)
    return render(request, 'production/production_create.html', {
        'orders': orders,
    })

@login_required
def production_edit(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)
    form = ProductionStageForm(request.POST or None, instance=stage)
    if form.is_valid():
        form.save()
        return redirect('production:production_detail', pk=pk)
    return render(request, 'production/production_form.html', {
        'form': form,
        'editing': True,
        'stage': stage,
    })

@login_required
def production_delete(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)
    if request.method == 'POST':
        stage.delete()
        return redirect('production:production_list')
    return redirect('production:production_detail', pk=pk)

@login_required
def production_export(request):
    stages = ProductionStage.objects.select_related('order','order__customer')
    rows = []
    for s in stages:
        row = {
            'Order Ref': s.order.reference,
            'Customer': s.order.customer.name,
        }
        for f in STATUS_FIELDS:
            row[f"{f.title()} Status"] = getattr(s, f"get_{f}_status_display")()
        rows.append(row)
    df = pd.DataFrame(rows)
    resp = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    resp['Content-Disposition'] = 'attachment; filename=production_list.xlsx'
    df.to_excel(resp, index=False)
    return resp

@login_required
def production_detail_list(request):
    f = ProductionStageFilter(
        request.GET,
        queryset=ProductionStage.objects.select_related('order','order__customer')
    )
    badge_colors = {
        st.id: {
            f: get_badge_color(getattr(st, f"{f}_status"))
            for f in STATUS_FIELDS
        } for st in f.qs
    }
    return render(request, 'production/production_detail_list.html', {
        'filter': f,
        'stages': f.qs,
        'status_fields': STATUS_FIELDS,
        'badge_colors': badge_colors,
    })

@login_required
def production_detail_export(request):
    f = ProductionStageFilter(
        request.GET,
        queryset=ProductionStage.objects.select_related('order','order__customer')
    )
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename=\"detailed_production_list.csv\"'
    writer = csv.writer(resp)
    # Header
    writer.writerow(
        ["Order Ref", "Customer"] +
        [f"{s.title()} Status" for s in STATUS_FIELDS] +
        [f"{s.title()} Target Date" for s in STATUS_FIELDS]
    )
    # Rows
    for st in f.qs:
        row = [st.order.reference, st.order.customer.name]
        for s in STATUS_FIELDS:
            row.append(getattr(st, f"get_{s}_status_display")())
        for s in STATUS_FIELDS:
            row.append(getattr(st, f"{s}_target_date"))
        writer.writerow(row)
    return resp

@csrf_exempt
@require_POST
def update_target_date(request, stage_id):
    field = request.POST.get('field')
    value = request.POST.get('value')
    stage = get_object_or_404(ProductionStage, pk=stage_id)
    if not field.endswith('_target_date') or not hasattr(stage, field):
        return HttpResponseBadRequest("Invalid field")
    try:
        dt = datetime.strptime(value, "%Y-%m-%d").date()
        setattr(stage, field, dt)
        stage.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return HttpResponseBadRequest(str(e))

@csrf_exempt
@require_POST
@login_required
def production_update_status(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)
    data = json.loads(request.body)
    status_field = data.get('status_field')
    new_value = data.get('new_value')
    if not status_field or not hasattr(stage, status_field):
        return JsonResponse({'success': False, 'error': 'Invalid field'}, status=400)
    if status_field.endswith('_status'):
        stage_name = status_field.replace('_status','')
        update_stage_status(stage, stage_name, new_value)
        return JsonResponse({
            'success': True,
            'stage_id': stage.id,
            'status_field': status_field,
            'new_value': new_value
        })
    return JsonResponse({'success': False, 'error': 'Invalid field name'}, status=400)
