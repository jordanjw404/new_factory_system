import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from .utils import generate_barcode_image

# FactoryArea represents a physical area within the factory (e.g., Warehouse, Shop Floor)
class FactoryArea(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Factory Areas'

    def __str__(self):
        return self.name


# Location represents a specific location within a factory area, like a shelf, bay, or storage rack
class Location(models.Model):
    name = models.CharField(max_length=100)
    area = models.ForeignKey(FactoryArea, on_delete=models.CASCADE, related_name="locations")
    is_active = models.BooleanField(default=True)
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Max storage units")

    class Meta:
        unique_together = ('name', 'area')
        ordering = ['area__name', 'name']

    def clean(self):
        # Prevent a location from being its own area (data integrity check)
        if self.pk and self.area_id == self.pk:
            raise ValidationError("Location cannot be its own area")

    def __str__(self):
        return f"{self.area.name} → {self.name}"


# Supplier represents suppliers for raw materials and components, including contact details
class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    default_lead_time = models.PositiveIntegerField(help_text="Days until delivery", default=5)
    is_active = models.BooleanField(default=True)
    rating = models.PositiveSmallIntegerField(
        choices=[(1, 'Poor'), (2, 'Average'), (3, 'Good'), (4, 'Excellent')],
        default=3
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (Lead: {self.default_lead_time}d)"


# Item represents an inventory item, including boards, edge banding, cabinets, and general stock
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
    width = models.PositiveIntegerField(null=True, blank=True, help_text="mm")
    length = models.PositiveIntegerField(null=True, blank=True, help_text="mm")
    height = models.PositiveIntegerField(null=True, blank=True, help_text="mm")
    thickness = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="mm")
    unit = models.CharField(max_length=10, default="PCS")
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    safety_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_order_qty = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    is_active = models.BooleanField(default=True)
    standard_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    barcode_value = models.CharField(max_length=50, unique=True, blank=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    color = models.CharField(max_length=100, blank=True)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.SET_NULL)
    supplier_code = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['type', 'code']
        indexes = [
            models.Index(fields=['type', 'is_active']),
            models.Index(fields=['code']),
        ]

    def save(self, *args, **kwargs):
        # Generate barcode if missing
        if not self.barcode_value:
            self.barcode_value = str(uuid.uuid4().int)[:12]
            self.barcode_image = generate_barcode_image(self.barcode_value)
        super().save(*args, **kwargs)

    @property
    def total_stock(self):
        # Calculates total available stock across all locations
        return self.stock_levels.aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def needs_reorder(self):
        # Checks if stock is below the reorder level
        return self.total_stock <= self.reorder_level

    def __str__(self):
        return f"{self.code} - {self.name} ({self.get_type_display()})"


# BoardStock tracks individual pieces of board, including offcuts, with dimensional details
class BoardStock(models.Model):
    parent_board = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        limit_choices_to={'type': Item.ItemType.BOARD},
        related_name='pieces'
    )
    dimensions = models.JSONField(default=dict)  # Stores length, width, thickness
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    is_offcut = models.BooleanField(default=True)
    allocated_to = models.ForeignKey(
        'orders.Order', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='allocated_stock'
    )
    barcode_value = models.CharField(max_length=50, unique=True, blank=True)
    barcode_image = models.ImageField(upload_to='barcodes/boardstock/', blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['parent_board__code', '-created_at']
        verbose_name_plural = 'Board Stock'

    @property
    def length(self):
        return self.dimensions.get('length', 0)

    @property
    def width(self):
        return self.dimensions.get('width', 0)

    @property
    def area(self):
        return self.length * self.width

    @property
    def full_sheet_area(self):
        # Use the parent board dimensions
        if self.parent_board.width and self.parent_board.length:
            return self.parent_board.width * self.parent_board.length
        raise ValidationError("Parent board must have width and length defined.")

    @property
    def estimated_price(self):
        # Ensure the parent board has a standard cost
        if not self.parent_board.standard_cost:
            raise ValidationError(f"Parent board {self.parent_board.code} does not have a standard cost set.")

        # Calculate the price proportionally based on area
        full_price = self.parent_board.standard_cost
        piece_area = self.area
        full_area = self.full_sheet_area
        
        if full_area == 0:
            raise ValidationError("Full sheet area cannot be zero.")

        # Price is proportional to the piece size
        return round((piece_area / full_area) * full_price, 2)

    def __str__(self):
        return f"{self.parent_board.code} - {self.length}x{self.width}mm"

# ItemStock tracks the quantity of each item at different locations
class ItemStock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="stock_levels")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="stock_levels")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_checked = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('item', 'location')
        verbose_name_plural = 'Item Stock Levels'
        ordering = ['item__name', 'location__name']
        indexes = [
            models.Index(fields=['item', 'location']),
        ]

    def __str__(self):
        return f"{self.item.code} @ {self.location.name}: {self.quantity}"

# Movement tracks inventory movements (stock in, stock out, transfers, adjustments)
class Movement(models.Model):
    class MovementType(models.TextChoices):
        IN = 'IN', 'Stock In'
        OUT = 'OUT', 'Stock Out'
        TRANSFER = 'TRANSFER', 'Transfer'
        ADJUSTMENT = 'ADJUSTMENT', 'Adjustment'

    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="movements")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    move_type = models.CharField(max_length=10, choices=MovementType.choices)
    from_location = models.ForeignKey(Location, null=True, blank=True, related_name='moves_from', on_delete=models.PROTECT)
    to_location = models.ForeignKey(Location, null=True, blank=True, related_name='moves_to', on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    approved = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['item', 'move_type', 'timestamp']),
        ]

    def clean(self):
        """Validate movement logic before saving."""
        if self.move_type == self.MovementType.TRANSFER:
            if not self.from_location or not self.to_location:
                raise ValidationError("Transfers require both source and destination locations")
            if self.from_location == self.to_location:
                raise ValidationError("Cannot transfer to the same location")
                
        elif self.move_type == self.MovementType.IN:
            if not self.to_location:
                raise ValidationError("Stock IN requires a destination location")
            if self.from_location:
                raise ValidationError("Stock IN should not have a source location")
                
        elif self.move_type == self.MovementType.OUT:
            if not self.from_location:
                raise ValidationError("Stock OUT requires a source location")
            if self.to_location:
                raise ValidationError("Stock OUT should not have a destination location")

    def __str__(self):
        return f"{self.get_move_type_display()} - {self.item.code} x{self.quantity}"

# IncomingOrder tracks purchase orders from suppliers
class IncomingOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="incoming_orders")
    order_ref = models.CharField(max_length=100, unique=True)
    expected_date = models.DateField()
    received_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="PENDING", choices=[
        ("PENDING", "Pending"),
        ("PARTIAL", "Partially Received"),
        ("RECEIVED", "Fully Received"),
        ("CANCELLED", "Cancelled")
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_ref} from {self.supplier.name}"

    @property
    def total_items(self):
        # Calculate the total number of items in the order
        return self.items.aggregate(total=models.Sum('quantity_expected'))['total'] or 0

    @property
    def total_received(self):
        # Calculate the total number of items received
        return self.items.aggregate(received=models.Sum('quantity_received'))['received'] or 0

    @property
    def is_fully_received(self):
        # Check if all items have been received
        return self.total_items == self.total_received


class IncomingOrderItem(models.Model):
    order = models.ForeignKey(IncomingOrder, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="incoming_order_items")
    quantity_expected = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="incoming_order_items")
    received = models.BooleanField(default=False)

    # Correct way to handle timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'item']
        unique_together = ('order', 'item', 'location')

    def __str__(self):
        return f"{self.item.name} (Order {self.order.order_ref})"

    def save(self, *args, **kwargs):
        # Automatically mark the item as received if fully received
        if self.quantity_received >= self.quantity_expected:
            self.received = True

        super().save(*args, **kwargs)

