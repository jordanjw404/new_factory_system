import os
import uuid
from django.db import models
from django.conf import settings
import barcode
from barcode.writer import ImageWriter


class BarcodeMixin(models.Model):
    barcode = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)
    barcode_image = models.ImageField(upload_to="barcodes/", blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Generate barcode before saving if not already set
        if not self.barcode_image:
            self.generate_barcode_image()
        super().save(*args, **kwargs)

    def generate_barcode_image(self):
        # Ensure barcode directory exists
        barcode_dir = os.path.join(settings.MEDIA_ROOT, "barcodes")
        os.makedirs(barcode_dir, exist_ok=True)

        # Construct the file path
        filename = f"{self.barcode}.png"
        full_path = os.path.join(barcode_dir, filename)

        # Get barcode class and generate image
        code128 = barcode.get_barcode_class('code128')
        code = code128(str(self.barcode), writer=ImageWriter())
        code.save(full_path[:-4])  # python-barcode adds .png itself

        # Set the image path relative to MEDIA_ROOT
        self.barcode_image = f"barcodes/{filename}"
