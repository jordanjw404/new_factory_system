from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order


@receiver(post_save, sender=Order)
def create_production_stage_on_send(sender, instance, created, **kwargs):
    if instance.send_to_production:
        instance.maybe_create_production_stage()
