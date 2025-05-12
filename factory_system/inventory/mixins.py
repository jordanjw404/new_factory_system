import os
import uuid
from django.db import models
from django.conf import settings
from barcode import Code128
from barcode.writer import ImageWriter


class BarcodeMixin(models.Model):
    barcode = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)
    barcode_image = models.ImageField(upload_to="barcodes/", blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Generate barcode image if not already set
        if not self.barcode_image:
            self.generate_barcode_image()
        
        super().save(*args, **kwargs)

    def generate_barcode_image(self):
        barcode_path = os.path.join(settings.MEDIA_ROOT, "barcodes")
        os.makedirs(barcode_path, exist_ok=True)

        barcode_filename = f"{self.barcode}.png"
        barcode_filepath = os.path.join(barcode_path, barcode_filename)

        # Generate the barcode image
        code128 = Code128(self.barcode, writer=ImageWriter())
        code128.save(barcode_filepath)

        # Set the image field
        self.barcode_image = f"barcodes/{barcode_filename}"
