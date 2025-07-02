# production/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order, ProductionStage
from .utils import create_production_stage


@receiver(post_save, sender=Order)
def trigger_production_creation(sender, instance, created, **kwargs):
    """
    Creates production stage when order is marked for production
    Ensures only one production stage is created per order
    """
    if instance.send_to_production:
        # Check if production stage already exists
        if not ProductionStage.objects.filter(order=instance).exists():
            create_production_stage(instance)
