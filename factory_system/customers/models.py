from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # if using Django's auth User for created_by

class Customer(models.Model):
    name = models.CharField(max_length=255, help_text="Company or Customer name")
    contact_name = models.CharField("Contact Person", max_length=255, blank=True)
    email = models.EmailField(unique=True)  # Unique contact email for the customer
    phone = models.CharField("Phone Number", max_length=20, blank=True)
    mobile = models.CharField("Mobile Number", max_length=20, blank=True)
    address_1 = models.TextField(blank=True, help_text="Mailing address for the customer")
    address_2 = models.TextField(blank=True, help_text="Mailing address for the customer")
    notes = models.TextField(blank=True, help_text="Internal notes about the customer")
    is_active = models.BooleanField(default=True, help_text="Active status of the customer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        help_text="User who added this customer"
    )

    def __str__(self):
        return self.name  # Use the customer name for easy identification

    def get_full_contact(self):
        """Return a one-line summary of the primary contact."""
        return f"{self.contact_name} <{self.email}>"

    class Meta:
        ordering = ["name"]  # Default ordering by name for convenience
        indexes = [
            models.Index(fields=["name"]),   # Index on name for fast lookup
            models.Index(fields=["email"]),  # Index on email for fast lookup
        ]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
