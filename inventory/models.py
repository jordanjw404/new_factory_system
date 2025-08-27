import uuid
from decimal import Decimal
from django.db import models

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory_product"
        ordering = ["sku"]

    def __str__(self):
        return f"{self.sku} — {self.name}"


class Balance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="balances")
    location_code = models.CharField(max_length=64, help_text="e.g. PICK-A01-B01-L01")
    qty_on_hand = models.DecimalField(max_digits=14, decimal_places=3, default=Decimal("0.000"))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inventory_balance"
        constraints = [
            models.UniqueConstraint(fields=["product", "location_code"], name="uq_product_location"),
        ]

    def __str__(self):
        return f"{self.product.sku}@{self.location_code}={self.qty_on_hand}"


class TxnType(models.TextChoices):
    IN = "IN", "IN"
    OUT = "OUT", "OUT"
    MOVE = "MOVE", "MOVE"


class StockTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="txns")
    txn_type = models.CharField(max_length=4, choices=TxnType.choices)
    qty = models.DecimalField(max_digits=14, decimal_places=3)
    from_location = models.CharField(max_length=64, blank=True, null=True)
    to_location = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory_stocktxn"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.txn_type} {self.qty} {self.product.sku}"
