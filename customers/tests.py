from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
 

from .models import Customer

class CustomerImportViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", password="testpass123"
        )
        self.client.login(username="tester", password="testpass123")

    def test_import_customers_csv_assigns_postcode(self):
        csv_content = (
            "Name,Email,Post Code\n"
            "Test Customer,test@example.com,AB12CD\n"
       )
        csv_file = SimpleUploadedFile(
            "customers.csv", csv_content.encode("utf-8"), content_type="text/csv"
        )

        response = self.client.post(
            reverse("customers:import_customers"), {"csv_file": csv_file}
        )

        self.assertRedirects(response, reverse("customers:customer_list"))
        customer = Customer.objects.get(email="test@example.com")
        self.assertEqual(customer.postcode, "AB12CD")
