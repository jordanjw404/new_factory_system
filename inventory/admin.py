from django.contrib import admin
from .models import Product, Balance, StockTransaction

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "created_at")
    search_fields = ("sku", "name")

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ("product", "location_code", "qty_on_hand", "updated_at")
    list_filter = ("location_code",)
    search_fields = ("product__sku", "product__name", "location_code")
    autocomplete_fields = ("product",)

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ("created_at", "txn_type", "product", "from_location", "to_location", "qty", "note")
    list_filter = ("txn_type",)
    date_hierarchy = "created_at"
    search_fields = ("product__sku", "product__name", "from_location", "to_location", "note")
