from datetime import timedelta
from django.utils import timezone
from .models import ProductionStage

def subtract_day_skip_weekend(date):
    """Adjust date to previous workday, skipping weekends"""
    date -= timedelta(days=1)
    if date.weekday() == 5:  # Saturday
        date -= timedelta(days=1)
    elif date.weekday() == 6:  # Sunday
        date -= timedelta(days=2)
    return date

def create_production_stage(order):
    """Create a ProductionStage and set target dates based on delivery."""
    if ProductionStage.objects.filter(order=order).exists():
        return ProductionStage.objects.get(order=order)

    delivery = order.delivery_date
    if hasattr(delivery, 'date'):
        delivery = delivery.date()

    stage = ProductionStage(order=order)

    # Calculate target dates in reverse order
    qc = subtract_day_skip_weekend(delivery)
    wrap = subtract_day_skip_weekend(qc)
    fit = subtract_day_skip_weekend(wrap)
    build = subtract_day_skip_weekend(fit)
    prep = subtract_day_skip_weekend(build)
    edge = subtract_day_skip_weekend(prep)
    nest = subtract_day_skip_weekend(edge)
    prog = subtract_day_skip_weekend(nest)
    sales = subtract_day_skip_weekend(prog)

    stage.quality_target_date = qc
    stage.wrapping_target_date = wrap
    stage.fittings_target_date = fit
    stage.build_target_date = build
    stage.prep_target_date = prep
    stage.edge_target_date = edge
    stage.nest_target_date = nest
    stage.programming_target_date = prog
    stage.sales_target_date = sales

    stage.estimated_nest_sheets = order.cabs * 0.55 + order.robes * 0.86 + order.panels * 0.1
    stage.estimated_build_cabs = order.cabs + order.robes

    stage.sales_status = 'NOT_STARTED'
    stage.programming_status = 'NOT_STARTED'
    stage.nest_status = 'NOT_STARTED'
    stage.edge_status = 'NOT_STARTED'
    stage.prep_status = 'NOT_STARTED'
    stage.build_status = 'NOT_STARTED'
    stage.fittings_status = 'NOT_STARTED'
    stage.wrapping_status = 'NOT_STARTED'
    stage.quality_status = 'NOT_STARTED'

    stage.save()
    return stage

def update_stage_status(production_stage, stage_name, new_status):
    """Update status and auto-set/unset completed date."""
    status_field = f"{stage_name}_status"
    completed_field = f"{stage_name}_completed_date"

    if not hasattr(production_stage, status_field):
        raise ValueError(f"Invalid stage name: {stage_name}")

    setattr(production_stage, status_field, new_status)

    if new_status == 'COMPLETED':
        if getattr(production_stage, completed_field) is None:
            setattr(production_stage, completed_field, timezone.now())
    else:
        if getattr(production_stage, completed_field):
            setattr(production_stage, completed_field, None)

    production_stage.save()

def all_stages_completed(production_stage):
    stages = [
        'sales_status', 'programming_status', 'nest_status', 'edge_status',
        'prep_status', 'build_status', 'fittings_status', 'wrapping_status', 'quality_status'
    ]
    return all(getattr(production_stage, stage) == 'COMPLETED' for stage in stages)

def get_current_stage(production_stage):
    stage_order = [
        'sales', 'programming', 'nest', 'edge', 'prep', 'build', 'fittings', 'wrapping', 'quality'
    ]
    for stage in stage_order:
        if getattr(production_stage, f"{stage}_status") != 'COMPLETED':
            return stage.capitalize()
    return "Complete"
