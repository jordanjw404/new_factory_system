from django.db import models
from orders.models import Order


class ProductionStage(models.Model):
    SALES_STATUS = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('STUCK', 'Stuck'),
        ('ON_HOLD', 'On Hold'),
        ('CONFIRMATION', 'Confirmation'),
        ('COMPLETED', 'Completed'),
        ('NO_PAPERWORK', 'No Paperwork'),
    ]

    STAGE_STATUS = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('STUCK', 'Stuck'),
        ('ON_HOLD', 'On Hold'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
        ('READY', 'Ready'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='production_stage')

    # Stage fields
    sales_status = models.CharField(max_length=20, choices=SALES_STATUS, default='NOT_STARTED')
    programming_status = models.CharField(max_length=20, choices=STAGE_STATUS, default='NOT_STARTED')
    nest_status = models.CharField(max_length=20, choices=STAGE_STATUS, default='NOT_STARTED')
    edge_status = models.CharField(max_length=20, choices=STAGE_STATUS, default='NOT_STARTED')
    prep_status = models.CharField(max_length=20, choices=STAGE_STATUS, default='NOT_STARTED')
    build_status = models.CharField(max_length=20, choices=STAGE_STATUS, default='NOT_STARTED')
    fittings_status = models.CharField(max_length=20, choices=STAGE_STATUS, default='NOT_STARTED')
    wrapping_status = models.CharField(max_length=20, choices=STAGE_STATUS, default='NOT_STARTED')
    quality_status = models.CharField(max_length=20, choices=STAGE_STATUS, default='NOT_STARTED')

    # Target Dates
    sales_target_date = models.DateField(null=True, blank=True)
    programming_target_date = models.DateField(null=True, blank=True)
    nest_target_date = models.DateField(null=True, blank=True)
    edge_target_date = models.DateField(null=True, blank=True)
    prep_target_date = models.DateField(null=True, blank=True)
    build_target_date = models.DateField(null=True, blank=True)
    fittings_target_date = models.DateField(null=True, blank=True)
    wrapping_target_date = models.DateField(null=True, blank=True)
    quality_target_date = models.DateField(null=True, blank=True)

    # Completed Dates
    sales_completed_date = models.DateField(null=True, blank=True)
    programming_completed_date = models.DateField(null=True, blank=True)
    nest_completed_date = models.DateField(null=True, blank=True)
    edge_completed_date = models.DateField(null=True, blank=True)
    prep_completed_date = models.DateField(null=True, blank=True)
    build_completed_date = models.DateField(null=True, blank=True)
    fittings_completed_date = models.DateField(null=True, blank=True)
    wrapping_completed_date = models.DateField(null=True, blank=True)
    quality_completed_date = models.DateField(null=True, blank=True)

    # Workload Estimation
    estimated_nest_sheets = models.FloatField(default=0)
    actual_nest_sheets = models.FloatField(default=0)
    estimated_build_cabs = models.IntegerField(default=0)

    def __str__(self):
        return f"Production for Order: {self.order.reference}"

    class Meta:
        ordering = ['-order__delivery_date']

    def get_current_stage_name(self):
        stages = [
            ("Sales", self.sales_status),
            ("Programming", self.programming_status),
            ("Nest", self.nest_status),
            ("Edge", self.edge_status),
            ("Prep", self.prep_status),
            ("Build", self.build_status),
            ("Fittings", self.fittings_status),
            ("Wrapping", self.wrapping_status),
            ("Quality", self.quality_status),
        ]
        for i, (name, status) in enumerate(stages):
            if status != 'COMPLETED':
                if i == 0 or stages[i - 1][1] == 'COMPLETED':
                    return name
                return name
        return "Complete"

    def all_stages_completed(self):
        return all(
            status == 'COMPLETED' for status in [
                self.sales_status,
                self.programming_status,
                self.nest_status,
                self.edge_status,
                self.prep_status,
                self.build_status,
                self.fittings_status,
                self.wrapping_status,
                self.quality_status,
            ]
        )
