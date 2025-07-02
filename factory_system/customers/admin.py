from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_name", "email", "phone", "is_active", "created_at")
    list_filter = ("is_active", "created_at")  # Filters in sidebar
    search_fields = ("name", "contact_name", "email", "phone", "mobile")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")  # display timestamps as read-only
