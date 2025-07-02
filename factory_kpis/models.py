from django.db import models


# Create your models here.
class build_kpi(models.Model):
    build_id = models.CharField(max_length=100, unique=True)
    build_time = models.FloatField()
    build_quality = models.FloatField()
    build_cost = models.FloatField()

    def __str__(self):
        return f"Build KPI {self.build_id}"
