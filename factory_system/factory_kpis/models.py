from django.db import models

# Create your models here.
<<<<<<< HEAD
class build_kpi(models.Model):
    build_id = models.CharField(max_length=100, unique=True)
    build_time = models.FloatField()
    build_quality = models.FloatField()
    build_cost = models.FloatField()

    def __str__(self):
        return f"Build KPI {self.build_id}"
    
    
=======
class Build
>>>>>>> 43fa2f6 (Add employees and factory_kpis apps; create initial files and register in settings)
