from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from .utils import create_production_stage

@receiver(post_save, sender=Order)
def handle_order_production(sender, instance, created, **kwargs):
    """
    Creates production stage when order is marked for production.
    Only creates if it doesn't already exist.
    """
    if instance.send_to_production and not hasattr(instance, 'production_stage'):
        create_production_stage(instance)
