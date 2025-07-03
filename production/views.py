# production/views.py
import csv
import json
from datetime import datetime, timedelta

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from orders.models import Order

from .filters import ProductionStageFilter
from .forms import ProductionStageForm
from .models import ProductionStage
from .utils import update_stage_status


def get_badge_color(status):
    return {
        "NOT_STARTED": "secondary",
        "IN_PROGRESS": "warning",
        "STUCK": "danger",
        "ON_HOLD": "dark",
        "COMPLETED": "success",
        "READY": "info",
        "CONFIRMATION": "primary",
        "NO_PAPERWORK": "danger",
    }.get(status, "secondary")


@login_required
def production_detail(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)
    context = {
        "stage": stage,
        "badge_colors": {
            f"{field}_status": get_badge_color(getattr(stage, f"{field}_status"))
            for field in [
                "sales",
                "programming",
                "nest",
                "edge",
                "prep",
                "build",
                "fittings",
                "wrapping",
                "quality",
            ]
        },
    }
    return render(request, "production/production_detail.html", context)


@login_required
def production_list(request):
    stages = ProductionStage.objects.select_related("order", "order__customer")
    status_fields = [
        "sales",
        "programming",
        "nest",
        "edge",
        "prep",
        "build",
        "fittings",
        "wrapping",
        "quality",
    ]
    badge_colors = {
        stage.id: {
            field: get_badge_color(getattr(stage, f"{field}_status"))
            for field in status_fields
        }
        for stage in stages
    }
    return render(
        request,
        "production/production_list.html",
        {
            "stages": stages,
            "badge_colors": badge_colors,
            "status_fields": status_fields,
        },
    )


@login_required
def production_edit(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)
    form = ProductionStageForm(request.POST or None, instance=stage)
    if form.is_valid():
        form.save()
        return redirect("production:production_detail", pk=pk)
    return render(
        request,
        "production/production_form.html",
        {"form": form, "editing": True, "stage": stage},
    )


@login_required
def production_create(request):
    form = ProductionStageForm(request.POST or None)
    if form.is_valid():
        production_stage = form.save(commit=False)
        delivery_date = production_stage.order.delivery_date

        if delivery_date:

            def weekday_back(d, days):
                d -= timedelta(days=days)
                while d.weekday() > 4:
                    d -= timedelta(days=1)
                return d

            stage_offsets = [14, 9, 8, 7, 6, 5, 4, 3, 2]  # sales to quality
            target_fields = [
                "sales",
                "programming",
                "nest",
                "edge",
                "prep",
                "build",
                "fittings",
                "wrapping",
                "quality",
            ]

            for field, offset in zip(target_fields, stage_offsets):
                setattr(
                    production_stage,
                    f"{field}_target_date",
                    weekday_back(delivery_date, offset),
                )

            production_stage.estimated_nest_sheets = (
                production_stage.order.cabs * 0.55
                + production_stage.order.robes * 0.86
                + production_stage.order.panels * 0.1
            )
            production_stage.estimated_build_cabs = (
                production_stage.order.cabs + production_stage.order.robes
            )

        production_stage.save()
        return redirect("production:production_list")

    return render(request, "production/production_form.html", {"form": form})


@login_required
def production_delete(request, pk):
    stage = get_object_or_404(ProductionStage, pk=pk)
    if request.method == "POST":
        stage.delete()
        return redirect("production:production_list")
    return redirect("production:production_detail", pk=pk)


@login_required
def production_export(request):
    stages = ProductionStage.objects.select_related("order", "order__customer")
    data = [
        {
            "Order Ref": s.order.reference,
            "Customer": s.order.customer.name,
            "Sales Status": s.get_sales_status_display(),
            "Programming Status": s.get_programming_status_display(),
            "Nest Status": s.get_nest_status_display(),
            "Edge Status": s.get_edge_status_display(),
            "Prep Status": s.get_prep_status_display(),
            "Build Status": s.get_build_status_display(),
            "Fittings Status": s.get_fittings_status_display(),
            "Wrapping Status": s.get_wrapping_status_display(),
            "Quality Status": s.get_quality_status_display(),
        }
        for s in stages
    ]
    df = pd.DataFrame(data)
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=production_list.xlsx"
    df.to_excel(response, index=False)
    return response


@login_required
def production_detail_list(request):
    f = ProductionStageFilter(
        request.GET,
        queryset=ProductionStage.objects.select_related("order", "order__customer"),
    )
    status_fields = [
        "sales",
        "programming",
        "nest",
        "edge",
        "prep",
        "build",
        "fittings",
        "wrapping",
        "quality",
    ]
    badge_colors = {
        stage.id: {
            field: get_badge_color(getattr(stage, f"{field}_status"))
            for field in status_fields
        }
        for stage in f.qs
    }
    return render(
        request,
        "production/production_detail_list.html",
        {
            "filter": f,
            "stages": f.qs,
            "status_fields": status_fields,
            "badge_colors": badge_colors,
        },
    )


@login_required
def production_detail_export(request):
    f = ProductionStageFilter(
        request.GET,
        queryset=ProductionStage.objects.select_related("order", "order__customer"),
    )
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="detailed_production_list.csv"'
    )
    writer = csv.writer(response)

    headers = (
        ["Order Ref", "Customer"]
        + [
            f"{stage.title()} Status"
            for stage in [
                "sales",
                "programming",
                "nest",
                "edge",
                "prep",
                "build",
                "fittings",
                "wrapping",
                "quality",
            ]
        ]
        + [
            f"{stage.title()} Target Date"
            for stage in [
                "sales",
                "programming",
                "nest",
                "edge",
                "prep",
                "build",
                "fittings",
                "wrapping",
                "quality",
            ]
        ]
    )

    writer.writerow(headers)

    for s in f.qs:
        row = [s.order.reference, s.order.customer.name]
        for stage in [
            "sales",
            "programming",
            "nest",
            "edge",
            "prep",
            "build",
            "fittings",
            "wrapping",
            "quality",
        ]:
            row.append(getattr(s, f"get_{stage}_status_display")())
        for stage in [
            "sales",
            "programming",
            "nest",
            "edge",
            "prep",
            "build",
            "fittings",
            "wrapping",
            "quality",
        ]:
            row.append(getattr(s, f"{stage}_target_date"))
        writer.writerow(row)

    return response


@csrf_exempt
@require_POST
def update_target_date(request, stage_id):
    field = request.POST.get("field")
    value = request.POST.get("value")
    stage = get_object_or_404(ProductionStage, pk=stage_id)

    if not field.endswith("_target_date") or not hasattr(stage, field):
        return HttpResponseBadRequest("Invalid field")

    try:
        setattr(stage, field, datetime.strptime(value, "%Y-%m-%d").date())
        stage.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return HttpResponseBadRequest(f"Failed to save: {str(e)}")


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