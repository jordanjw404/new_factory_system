import uuid
from django.db import models
from django.conf import settings
from .utils import generate_barcode_image


class FactoryArea(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    area = models.ForeignKey(FactoryArea, on_delete=models.CASCADE, related_name="locations")

    class Meta:
        unique_together = ('name', 'area')

    def __str__(self):
        return f"{self.area.name} - {self.name}"


class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    default_lead_time = models.PositiveIntegerField(help_text="Days until delivery", default=5)

    def __str__(self):
        return self.name


class Item(models.Model):
    class ItemType(models.TextChoices):
        BOARD = 'BOARD', 'Board'
        EDGE = 'EDGE', 'Edge Banding'
        CABINET = 'CABINET', 'Cabinet'
        STOCK = 'STOCK', 'General Stock'

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=ItemType.choices)
    description = models.TextField(blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    length = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    thickness = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=10, default="PCS")
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    barcode_value = models.CharField(max_length=50, unique=True, blank=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.barcode_value:
            self.barcode_value = str(uuid.uuid4().int)[:12]
        super().save(*args, **kwargs)
        if not self.barcode_image:
            barcode_file = generate_barcode_image(self.barcode_value)
            self.barcode_image.save(f"{self.code}.png", barcode_file, save=False)
            super().save(update_fields=["barcode_image"])

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        ordering = ['type', 'code']


class ItemStock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="stock_levels")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="stock_levels")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('item', 'location')

    def __str__(self):
        return f"{self.item.code} @ {self.location} = {self.quantity} {self.item.unit}"


class Movement(models.Model):
    class MovementType(models.TextChoices):
        IN = 'IN', 'Stock In'
        OUT = 'OUT', 'Stock Out'
        TRANSFER = 'TRANSFER', 'Transfer'

    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    from_location = models.ForeignKey(Location, null=True, blank=True, related_name='moves_from', on_delete=models.PROTECT)
    to_location = models.ForeignKey(Location, null=True, blank=True, related_name='moves_to', on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    move_type = models.CharField(max_length=10, choices=MovementType.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    reason = models.TextField(blank=True)
    approved = models.BooleanField(default=True)
    order_ref = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.move_type}: {self.quantity} {self.item.code} by {self.user.username} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class IncomingOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='incoming_orders')
    order_ref = models.CharField(max_length=100, blank=True)
    expected_date = models.DateField()
    delivery_eta = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    received = models.BooleanField(default=False)

    def __str__(self):
        return f"PO#{self.id} from {self.supplier.name}"


class IncomingOrderItem(models.Model):
    order = models.ForeignKey(IncomingOrder, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity_expected = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    barcode = models.CharField(max_length=50, blank=True)
    is_missing = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = str(uuid.uuid4().int)[:12]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.code} x {self.quantity_expected} → {self.location}"
