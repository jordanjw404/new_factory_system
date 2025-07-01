from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer
from django.db.models import TextChoices
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


class Order(models.Model):

    def maybe_create_production_stage(self):
        from production.models import ProductionStage
        from production.utils import create_production_stage

        if self.send_to_production and not hasattr(self, 'production_stage'):
            create_production_stage(self)

    class Priority(TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')
        URGENT = 'URGENT', _('Urgent')

    class OrderType(TextChoices):
        KITCHEN = 'KITCHEN', _('Kitchen')
        BEDROOM = 'BEDROOM', _('Bedroom')
        NON_PRODUCTION = 'NON_PRODUCTION', _('Non-Production')

    class Status(TextChoices):
        NO_PAPERWORK = 'NO_PAPERWORK', _('No Paperwork')
        AWAITING_DEPOSIT = 'AWAITING_DEPOSIT', _('Awaiting Deposit')
        IN_PRODUCTION = 'IN_PRODUCTION', _('In Production')
        READY_FOR_DELIVERY = 'READY_FOR_DELIVERY', _('Ready for Delivery')
        DELIVERED = 'DELIVERED', _('Delivered')
        ON_HOLD = 'ON_HOLD', _('On Hold')
        CANCELLED = 'CANCELLED', _('Cancelled')

    name = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    reference = models.CharField(max_length=100, help_text="Sales order reference")
    delivery_date = models.DateField(null=True, blank=True, help_text="Expected delivery or collection date")
    is_collection = models.BooleanField(default=False)
    order_type = models.CharField(max_length=20, choices=OrderType.choices, default=OrderType.KITCHEN)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.NO_PAPERWORK)
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        help_text="Priority of the order"
    )
    robes = models.PositiveIntegerField(default=0)
    cabs = models.PositiveIntegerField(default=0)
    panels = models.PositiveIntegerField(default=0)
    send_to_production = models.BooleanField(default=False, help_text="Tick to generate a production order.")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_orders')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.reference} - {self.name} [{self.customer.name}]"


class OrderAttachment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(
        upload_to='order_attachments/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Attachment for {self.order.reference}"


class OrderLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.action}"
