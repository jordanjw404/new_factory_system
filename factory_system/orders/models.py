from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer


class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('KITCHEN', 'Kitchen'),
        ('BEDROOM', 'Bedroom'),
        ('NON_PRODUCTION', 'Non-Production'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PRODUCTION', 'In Production'),
        ('COMPLETE', 'Complete'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('ON_HOLD', 'On Hold'),
    ]

    name = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    reference = models.CharField(max_length=100, help_text="Sales order reference")
    delivery_date = models.DateField(help_text="Expected delivery or collection date")
    is_collection = models.BooleanField(default=False)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='KITCHEN')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    robes = models.PositiveIntegerField(default=0)
    cabs = models.PositiveIntegerField(default=0)
    panels = models.PositiveIntegerField(default=0)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_orders')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} - {self.name} ({self.customer.name})"


class OrderAttachment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='order_attachments/')
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
