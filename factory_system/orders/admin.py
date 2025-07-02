from django.contrib import admin

from .models import Order, OrderAttachment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "reference", "status", "delivery_date")
    list_filter = ("status", "order_type", "delivery_date")
    search_fields = ("reference", "name", "customer__name")
    autocomplete_fields = ("customer",)


@admin.register(OrderAttachment)
class OrderAttachmentAdmin(admin.ModelAdmin):
    list_display = ("order", "file", "uploaded_at")
