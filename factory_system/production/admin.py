from django.contrib import admin

from .models import ProductionStage


@admin.register(ProductionStage)
class ProductionStageAdmin(admin.ModelAdmin):
    list_display = (
        "order_reference",
        "customer_name",
        "sales_status",
        "programming_status",
        "nest_status",
        "edge_status",
        "build_status",
        "quality_status",
    )
    list_filter = (
        "sales_status",
        "programming_status",
        "nest_status",
        "edge_status",
        "build_status",
        "quality_status",
    )
    search_fields = ("order__reference", "order__customer__name")
    autocomplete_fields = ("order",)
    readonly_fields = ("estimated_nest_sheets", "estimated_build_cabs")

    def order_reference(self, obj):
        return obj.order.reference

    order_reference.short_description = "Order Ref"

    def customer_name(self, obj):
        return obj.order.customer.name

    customer_name.short_description = "Customer"
