from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from customers.models import Customer
from orders.models import Order


class OrderCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com",
            phone="0123456789",
            contact_name="Test Contact",
        )

    def test_order_create_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("orders:order_create"), {
            "name": "Test Order",
            "customer": self.customer.id,
            "reference": "REF123",
            "delivery_date": "2025-05-01",
            "order_type": "KITCHEN",
            "status": "NO_PAPERWORK",
            "robes": 3,
            "cabs": 5,
            "panels": 7,
            "owner": self.user.id,
        })

        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.name, "Test Order")
