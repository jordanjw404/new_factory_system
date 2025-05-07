from django.contrib import admin
from .models import Supplier, Item, Location, ItemStock, Movement, BoardStock, IncomingOrder, IncomingOrderItem

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "type", "unit", "reorder_level", "barcode_value")

@admin.register(ItemStock)
class ItemStockAdmin(admin.ModelAdmin):
    list_display = ("item", "location", "quantity", "last_checked")
    list_filter = ("location", "item__type")
    search_fields = ("item__code", "item__name", "location__name")
    readonly_fields = ("last_checked",)

@admin.register(BoardStock)
class BoardStockAdmin(admin.ModelAdmin):
    list_display = ("parent_board", "location", "is_offcut", "area", "estimated_price", "created_at", "modified_at")
    list_filter = ("location", "is_offcut")
    search_fields = ("parent_board__code", "location__name")
    readonly_fields = ("barcode_image",)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_email", "phone", "default_lead_time", "rating")
    search_fields = ("name", "contact_email", "phone")
    list_filter = ("rating",)

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ("item", "move_type", "quantity", "from_location", "to_location", "timestamp", "user", "approved")
    list_filter = ("move_type", "approved", "from_location", "to_location", "item")
    search_fields = ("item__code", "item__name", "reference", "user__username")
    readonly_fields = ("timestamp",)

@admin.register(IncomingOrder)
class IncomingOrderAdmin(admin.ModelAdmin):
    list_display = ("order_ref", "supplier", "expected_date", "status", "created_at")
    list_filter = ("status", "supplier")
    search_fields = ("order_ref", "supplier__name")

@admin.register(IncomingOrderItem)
class IncomingOrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "item", "quantity_expected", "quantity_received", "location", "received")
    list_filter = ("received", "location")
    search_fields = ("order__order_ref", "item__name", "location__name")