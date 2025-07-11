# Generated by Django 5.2 on 2025-06-30 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_order_priority_order_send_to_production_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="priority",
            field=models.CharField(
                choices=[
                    ("LOW", "Low"),
                    ("MEDIUM", "Medium"),
                    ("HIGH", "High"),
                    ("URGENT", "Urgent"),
                ],
                default="MEDIUM",
                help_text="Priority of the order",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "Pending"),
                    ("IN_PRODUCTION", "In Production"),
                    ("COMPLETE", "Complete"),
                    ("DELIVERED", "Delivered"),
                    ("CANCELLED", "Cancelled"),
                    ("ON_HOLD", "On Hold"),
                ],
                default="PENDING",
                max_length=20,
            ),
        ),
    ]
