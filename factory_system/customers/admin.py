from django.contrib import admin
from .models import Customer
from orders.models import Order




@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_name", "email", "phone", "is_active", "created_at")
    list_filter = ("is_active", "created_at")  # Filters in sidebar
    search_fields = ("name", "contact_name", "email", "phone", "mobile")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")  # display timestamps as read-only

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "order_date")
    list_filter = ("order_date",)
    search_fields = ("id", "customer__name", "customer__email")
    ordering = ("-order_date",)
    autocomplete_fields = ("customer",)  # enables search-as-you-type for customer field
