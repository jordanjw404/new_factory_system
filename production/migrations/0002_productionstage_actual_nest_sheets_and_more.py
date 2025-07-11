# Generated by Django 5.2 on 2025-04-27 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("production", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="productionstage",
            name="actual_nest_sheets",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="productionstage",
            name="build_status",
            field=models.CharField(
                choices=[
                    ("NOT_STARTED", "Not Started"),
                    ("IN_PROGRESS", "In Progress"),
                    ("STUCK", "Stuck"),
                    ("ON_HOLD", "On Hold"),
                    ("CANCELLED", "Cancelled"),
                    ("COMPLETED", "Completed"),
                ],
                default="NOT_STARTED",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="productionstage",
            name="edge_status",
            field=models.CharField(
                choices=[
                    ("NOT_STARTED", "Not Started"),
                    ("IN_PROGRESS", "In Progress"),
                    ("STUCK", "Stuck"),
                    ("ON_HOLD", "On Hold"),
                    ("CANCELLED", "Cancelled"),
                    ("COMPLETED", "Completed"),
                ],
                default="NOT_STARTED",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="productionstage",
            name="fittings_status",
            field=models.CharField(
                choices=[
                    ("NOT_STARTED", "Not Started"),
                    ("IN_PROGRESS", "In Progress"),
                    ("STUCK", "Stuck"),
                    ("ON_HOLD", "On Hold"),
                    ("CANCELLED", "Cancelled"),
                    ("COMPLETED", "Completed"),
                ],
                default="NOT_STARTED",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="productionstage",
            name="nest_status",
            field=models.CharField(
                choices=[
                    ("NOT_STARTED", "Not Started"),
                    ("IN_PROGRESS", "In Progress"),
                    ("STUCK", "Stuck"),
                    ("ON_HOLD", "On Hold"),
                    ("CANCELLED", "Cancelled"),
                    ("COMPLETED", "Completed"),
                ],
                default="NOT_STARTED",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="productionstage",
            name="prep_status",
            field=models.CharField(
                choices=[
                    ("NOT_STARTED", "Not Started"),
                    ("IN_PROGRESS", "In Progress"),
                    ("STUCK", "Stuck"),
                    ("ON_HOLD", "On Hold"),
                    ("CANCELLED", "Cancelled"),
                    ("COMPLETED", "Completed"),
                ],
                default="NOT_STARTED",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="productionstage",
            name="programming_status",
            field=models.CharField(
                choices=[
                    ("NOT_STARTED", "Not Started"),
                    ("IN_PROGRESS", "In Progress"),
                    ("STUCK", "Stuck"),
                    ("ON_HOLD", "On Hold"),
                    ("CANCELLED", "Cancelled"),
                    ("COMPLETED", "Completed"),
                ],
                default="NOT_STARTED",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="productionstage",
            name="quality_status",
            field=models.CharField(
                choices=[
                    ("NOT_STARTED", "Not Started"),
                    ("IN_PROGRESS", "In Progress"),
                    ("STUCK", "Stuck"),
                    ("ON_HOLD", "On Hold"),
                    ("CANCELLED", "Cancelled"),
                    ("COMPLETED", "Completed"),
                ],
                default="NOT_STARTED",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="productionstage",
            name="sales_status",
            field=models.CharField(
                choices=[
                    ("NOT_STARTED", "Not Started"),
                    ("IN_PROGRESS", "In Progress"),
                    ("STUCK", "Stuck"),
                    ("ON_HOLD", "On Hold"),
                    ("CONFIRMATION", "Confirmation"),
                    ("COMPLETED", "Completed"),
                    ("NO_PAPERWORK", "No Paperwork"),
                ],
                default="NOT_STARTED",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="productionstage",
            name="wrapping_status",
            field=models.CharField(
                choices=[
                    ("NOT_STARTED", "Not Started"),
                    ("IN_PROGRESS", "In Progress"),
                    ("STUCK", "Stuck"),
                    ("ON_HOLD", "On Hold"),
                    ("CANCELLED", "Cancelled"),
                    ("COMPLETED", "Completed"),
                ],
                default="NOT_STARTED",
                max_length=20,
            ),
        ),
    ]
