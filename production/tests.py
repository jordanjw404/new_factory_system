# production/tests.py
import csv
import io
import json
from datetime import date, timedelta

import pandas as pd
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from orders.models import Order
from production.models import ProductionStage
from customers.models import Customer
from production.utils import create_production_stage, subtract_day_skip_weekend
User = get_user_model()

class ProductionViewsTests(TestCase):
    def setUp(self):
        # create a customer for Orders
        self.customer = Customer.objects.create(name="Test Cust")
        # create a test user and log in
        self.user = User.objects.create_user(username="joe", password="pass")
        self.client = Client()
        self.client.login(username="joe", password="pass")

        # create an order and auto-create its ProductionStage
        self.order = Order.objects.create(
            name="Test Order",
            customer=self.customer,
            reference="REF123",
            delivery_date=date.today() + timedelta(days=10),
            robes=2,
            cabs=3,
            panels=1,
            send_to_production=True,
        )
        # fire your signal
        self.order.maybe_create_production_stage()
        self.stage = self.order.production_stage

    def test_production_list_view(self):
        resp = self.client.get(reverse("production:production_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Production List")
        self.assertContains(resp, self.order.reference)

    def test_production_detail_view(self):
        resp = self.client.get(reverse("production:production_detail", args=[self.stage.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.order.reference)

    def test_production_edit_view_get_only(self):
        """Ensure the edit form renders on GET."""
        url = reverse("production:production_edit", args=[self.stage.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<form')  # form is present

    def test_production_delete_view(self):
        resp = self.client.post(reverse("production:production_delete", args=[self.stage.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(ProductionStage.objects.filter(pk=self.stage.id).exists())

    def test_production_export_view(self):
        resp = self.client.get(reverse("production:production_export"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        # read with pandas
        df = pd.read_excel(io.BytesIO(resp.content))
        self.assertIn("Order Ref", df.columns)
        self.assertIn(self.order.reference, df["Order Ref"].astype(str).tolist())

    def test_production_detail_list_view(self):
        resp = self.client.get(reverse("production:production_detail_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.order.reference)

    def test_production_detail_export_view(self):
        resp = self.client.get(reverse("production:production_detail_export"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "text/csv")
        reader = csv.reader(io.StringIO(resp.content.decode()))
        headers = next(reader)
        self.assertTrue(headers[0].startswith("Order Ref"))
        self.assertTrue(headers[1].startswith("Customer"))

    def test_update_status_endpoint(self):
        url = reverse("production:production_update_status", args=[self.stage.id])
        payload = {"status_field": "sales_status", "new_value": "COMPLETED"}
        resp = self.client.post(
            url, json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.stage.refresh_from_db()
        self.assertEqual(self.stage.sales_status, "COMPLETED")
        self.assertIsNotNone(self.stage.sales_completed_date)

    def test_update_target_date_endpoint(self):
        url = reverse("production:update_target_date", args=[self.stage.id])
        new_date = (date.today() + timedelta(days=5)).isoformat()
        resp = self.client.post(url, {"field": "nest_target_date", "value": new_date})
        self.assertEqual(resp.status_code, 200)
        self.stage.refresh_from_db()
        self.assertEqual(self.stage.nest_target_date.isoformat(), new_date)

class ProductionTargetDatesTests(TestCase):
    def setUp(self):
        # create a customer
        self.customer = Customer.objects.create(name="Cust A")
        # make an order with a known delivery date
        self.order = Order.objects.create(
            name="Test Order",
            customer=self.customer,
            reference="TGT123",
            delivery_date=date(2025, 7, 11),  # Friday
            robes=0,
            cabs=0,
            panels=0,
            send_to_production=True,
        )

    def test_target_dates_chain(self):
        # run the util to build a ProductionStage
        stage = create_production_stage(self.order)

        delivery = self.order.delivery_date
        # according to your util:
        #   qc = subtract_day_skip_weekend(delivery)
        #   wrap = subtract_day_skip_weekend(qc)
        #   fit = subtract_day_skip_weekend(wrap)
        #   ... etc.
        expected_qc      = subtract_day_skip_weekend(delivery)                      # 2025-07-10 (Thu)
        expected_wrapping = subtract_day_skip_weekend(expected_qc)                   # 2025-07-09 (Wed)
        expected_fittings = subtract_day_skip_weekend(expected_wrapping)             # 2025-07-08 (Tue)

        self.assertEqual(stage.quality_target_date, expected_qc)
        self.assertEqual(stage.wrapping_target_date, expected_wrapping)
        self.assertEqual(stage.fittings_target_date, expected_fittings)

        # And sales is 9 steps back from nest, but you can at least spot‐check:
        # nest = subtract_day_skip_weekend(expected_edge) etc.
        # For brevity just check that sales_target_date is earlier than programming_target_date:
        self.assertLess(stage.sales_target_date, stage.programming_target_date)