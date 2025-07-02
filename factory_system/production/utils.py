# utils.py
"""
Utilities for creating and managing ProductionStage deadlines,
accounting for calendar offsets, weekends, and UK bank holidays.
Each stage inherits the previous target date, then subtracts calendar days,
adjusted for weekends and holidays.
"""
from datetime import date, datetime, timedelta
from typing import Dict, Optional, Any
import holidays
from django.utils import timezone
from .models import ProductionStage

# Function to get UK holidays for specific year
def get_uk_holidays(year: int) -> set:
    """Get UK holidays for specific year"""
    return set(holidays.UnitedKingdom(years=[year]).keys())

# Sequence of stages from closest to delivery backwards
STAGE_SEQUENCE = [
    'quality',
    'wrapping',
    'fittings',
    'build',
    'prep',
    'edge',
    'nest',
    'programming',
    'sales',
]

# Default calendar-day offsets per stage (days to subtract before adjustment)
DEFAULT_OFFSETS: Dict[str, int] = {
    'sales': 7,
    'programming': 2,
    'nest': 1,
    'edge': 1,
    'prep': 1,
    'build': 1,
    'fittings': 1,
    'wrapping': 1,
    'quality': 1,
}


def adjust_for_non_business(dt: date) -> date:
    """
    Continuously move dt back one day at a time until it's a valid business day:
      - Skip Saturdays & Sundays
      - Skip UK bank holidays
    """
    if not isinstance(dt, date):
        raise TypeError(f"Expected date, got {type(dt)}")
    
    # Get holidays for the relevant year
    uk_holidays = get_uk_holidays(dt.year)
    
    while dt.weekday() >= 5 or dt in uk_holidays:
        dt -= timedelta(days=1)
        # Check if we crossed into previous year
        if dt.year not in uk_holidays:
            uk_holidays = get_uk_holidays(dt.year)
    
    return dt


def subtract_and_adjust(start_dt: date, days: int) -> date:
    """
    Subtract `days` calendar days, then apply adjustment to business day.
    """
    if not isinstance(start_dt, date):
        raise TypeError(f"Expected date, got {type(start_dt)}")
    if not isinstance(days, int) or days < 0:
        raise ValueError(f"Days must be non-negative int, got {days}")
    
    # Calculate raw target date
    target = start_dt - timedelta(days=days)
    
    # Adjust to business day
    return adjust_for_non_business(target)


def compute_stage_targets(
    delivery_date: date,
    offsets: Optional[Dict[str, int]] = None
) -> Dict[str, date]:
    """
    Compute target dates sequentially from delivery_date using offsets:
    1. Start with delivery_date
    2. For each stage in reverse order:
        a. Subtract calendar days
        b. Adjust to business day
        c. Set as target for that stage
    3. Continue to next stage using adjusted date
    """
    if not isinstance(delivery_date, date):
        # Handle datetime objects
        if isinstance(delivery_date, datetime):
            delivery_date = delivery_date.date()
        else:
            raise TypeError("delivery_date must be date or datetime")
    
    # Prepare offsets (custom override defaults)
    stage_offsets = DEFAULT_OFFSETS.copy()
    if offsets:
        if not isinstance(offsets, dict):
            raise TypeError("Offsets must be dict of str->int")
        for stage, days in offsets.items():
            if stage not in DEFAULT_OFFSETS:
                raise KeyError(f"Unknown stage: {stage}")
            if not isinstance(days, int) or days < 0:
                raise ValueError(f"Offset for {stage} must be non-negative int")
            stage_offsets[stage] = days
    
    targets: Dict[str, date] = {}
    current_date = delivery_date
    
    # Process stages from delivery backwards
    for stage in STAGE_SEQUENCE:
        days = stage_offsets[stage]
        current_date = subtract_and_adjust(current_date, days)
        targets[stage] = current_date
    
    return targets


def create_production_stage(order: Any, offsets: Optional[Dict[str, int]] = None) -> ProductionStage:
    """
    Create or update production stage with date recalculation
    """
    obj, created = ProductionStage.objects.get_or_create(order=order)
    
    # Extract delivery date
    delivery = order.delivery_date
    if isinstance(delivery, datetime):
        delivery = delivery.date()
    
    # Calculate all stage targets
    targets = compute_stage_targets(delivery, offsets)
    
    # Apply targets to model
    for stage, target_date in targets.items():
        setattr(obj, f"{stage}_target_date", target_date)
    
    # Save delivery date used for calculations
    obj.original_delivery_date = delivery
    
    # Preserve existing statuses if updating
    if not created:
        # Only reset statuses if they haven't been set
        for stage in DEFAULT_OFFSETS:
            status_attr = f"{stage}_status"
            if not getattr(obj, status_attr) or getattr(obj, status_attr) == 'NOT_STARTED':
                setattr(obj, status_attr, 'NOT_STARTED')
    
    obj.save()
    return obj


def update_stage_status(production_stage: ProductionStage, stage_name: str, new_status: str) -> None:
    """
    Update stage status and completed_date.
    """
    status_field = f"{stage_name}_status"
    comp_field = f"{stage_name}_completed_date"
    
    if not hasattr(production_stage, status_field):
        raise ValueError(f"Invalid stage: {stage_name}")
    
    setattr(production_stage, status_field, new_status)
    
    # Update completed date
    if new_status == 'COMPLETED':
        if not getattr(production_stage, comp_field):
            setattr(production_stage, comp_field, timezone.now())
    else:
        # Clear completion date if status changed from COMPLETED
        if getattr(production_stage, comp_field):
            setattr(production_stage, comp_field, None)
    
    production_stage.save()


def all_stages_completed(production_stage: ProductionStage) -> bool:
    """Check if all production stages are completed"""
    return all(
        getattr(production_stage, f"{stage}_status") == 'COMPLETED'
        for stage in DEFAULT_OFFSETS
    )


def get_current_stage(production_stage: ProductionStage) -> str:
    """Get the first incomplete stage in production sequence"""
    # Follow forward sequence (reverse of STAGE_SEQUENCE)
    for stage in reversed(STAGE_SEQUENCE):
        if getattr(production_stage, f"{stage}_status") != 'COMPLETED':
            return stage.capitalize()
    return 'Complete'

def update_production_dates(production_stage: ProductionStage, new_delivery: date):
    """Update target dates without changing statuses"""
    targets = compute_stage_targets(new_delivery)
    
    # Update only target dates
    for stage, target_date in targets.items():
        setattr(production_stage, f"{stage}_target_date", target_date)
    
    production_stage.save()