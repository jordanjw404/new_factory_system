from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .mixins import BarcodeMixin
import uuid


class Supplier(models.Model):
    name = models.CharField(max_length=150)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cabinet(BarcodeMixin):
    CABINET_TYPES = [
        ('Base Unit', 'Base Unit'),
        ('Wall Unit', 'Wall Unit'),
        ('Tall Unit', 'Tall Unit'),
        ('Corner Unit', 'Corner Unit'),
        ('Drawer Unit', 'Drawer Unit'),
        ('Pull-Out Unit', 'Pull-Out Unit'),
    ]
    
    type = models.CharField(max_length=20, choices=CABINET_TYPES)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    depth = models.DecimalField(max_digits=10, decimal_places=2)
    colour = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} ({self.barcode})"


class Hardware(BarcodeMixin):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.barcode})"


class Board(BarcodeMixin):
    board_code = models.CharField(max_length=100, unique=True)
    colour = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    thickness = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    parent_board = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="offcuts")
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.board_code} ({self.barcode}) - {self.length}x{self.width}x{self.thickness}"


class EdgeBanding(BarcodeMixin):
    code = models.CharField(max_length=100, unique=True)
    colour = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    thickness = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} ({self.barcode})"


class Inventory(BarcodeMixin):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    quantity_on_hand = models.PositiveIntegerField(default=0)
    quantity_reserved = models.PositiveIntegerField(default=0)
    quantity_available = models.PositiveIntegerField(default=0)
    location = models.ForeignKey("Location", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.quantity_available = self.quantity_on_hand - self.quantity_reserved
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item} ({self.barcode}) - Quantity: {self.quantity_on_hand} - Location: {self.location}"


#Transaction is to track the transactions of the products
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'IN'),
        ('OUT', 'OUT'),
        ('MOVE', 'MOVE'),
    ]
    
    item_type = models.CharField(max_length=20, choices=[
        ('Cabinet', 'Cabinet'),
        ('Hardware', 'Hardware'),
        ('Board', 'Board'),
        ('Edge Banding', 'Edge Banding'),
    ])
    item_id = models.PositiveIntegerField()
    barcode = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    from_location = models.ForeignKey("inventory.Location", on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_from')
    to_location = models.ForeignKey("inventory.Location", on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_to')
    order = models.ForeignKey("inventory.Order", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.barcode} - Quantity: {self.quantity}"



#LOG is to track the logs of the transactions
class Log(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.transaction} at {self.created_at}"


#Location is to track the locations of the products
class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent_location = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="sub_locations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#Order is to track the orders of the products
class Order(models.Model):
    order_number = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=100)
    due_date = models.DateField()
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.customer_name}"
