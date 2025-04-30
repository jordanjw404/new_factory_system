from django.contrib import admin
from .models import Item, Location, ItemStock, Movement
from django.utils.html import format_html

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "type", "unit", "reorder_level", "barcode_preview")
    list_filter = ("type", "color")
    search_fields = ("code", "name", "description")
    readonly_fields = ("barcode_image",)

    def barcode_preview(self, obj):
        if obj.barcode_image:
            return format_html('<img src="{}" width="150" />', obj.barcode_image.url)
        return "No barcode"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ItemStock)
class ItemStockAdmin(admin.ModelAdmin):
    list_display = ("item", "location", "quantity")
    list_filter = ("location",)
    search_fields = ("item__code", "item__name")


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ("item", "move_type", "quantity", "from_location", "to_location", "timestamp", "user", "approved")
    list_filter = ("move_type", "approved", "from_location", "to_location", "item")
    search_fields = ("item__code", "item__name", "reason", "order_ref")
    readonly_fields = ("timestamp",)
