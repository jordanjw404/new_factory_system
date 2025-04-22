from django.db import models
from customers.models import Customer  # import the Customer model

class Order(models.Model):
    customer = models.ForeignKey(
        Customer, related_name="orders", on_delete=models.PROTECT
    )
    order_date = models.DateTimeField(auto_now_add=True)
    # ... other fields like total_amount, status, etc.

    def __str__(self):
        return f"Order #{self.id} for {self.customer.name}"
    
    class Meta:
        ordering = ["-order_date"]

