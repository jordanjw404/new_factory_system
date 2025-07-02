from django.contrib import admin

from .models import Board, Cabinet, EdgeBanding, Hardware, Inventory, Supplier


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "barcode",
        "item",
        "quantity_on_hand",
        "quantity_reserved",
        "quantity_available",
        "barcode_image_tag",
    )
    readonly_fields = ("barcode_image_tag",)

    def barcode_image_tag(self, obj):
        if obj.barcode_image:
            return f'<img src="{obj.barcode_image.url}" width="150" />'
        return "-"

    barcode_image_tag.short_description = "Barcode Image"
    barcode_image_tag.allow_tags = True


admin.site.register(Supplier)
admin.site.register(Cabinet)
admin.site.register(Hardware)
admin.site.register(Board)
admin.site.register(EdgeBanding)
