from django.db import models

class ProductionStage(models.Model):
    build_date = models.DateField()
    cabinet_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.build_date} - {self.cabinet_count} cabinets"
