from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from production.utils import create_production_stage

@receiver(post_save, sender=Order)
def handle_order_production(sender, instance, created, **kwargs):
    """
    Handles production stage creation/update when:
    - Order is newly created and marked for production
    - Existing order is updated to be marked for production
    - Delivery date changes on an order already in production
    """
    # If order is being sent to production
    if instance.send_to_production:
        # Create or update production stage
        create_production_stage(instance)
        
        # If delivery date changed, update production stage dates
        if not created and 'delivery_date' in instance.get_dirty_fields():
            # Only update if production stage exists
            if hasattr(instance, 'productionstage'):
                create_production_stage(instance)