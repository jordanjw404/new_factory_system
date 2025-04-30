import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile

def generate_barcode_image(barcode_value):
    CODE128 = barcode.get_barcode_class('code128')
    buffer = BytesIO()
    barcode_obj = CODE128(barcode_value, writer=ImageWriter())
    barcode_obj.write(buffer, options={'write_text': False})
    return ContentFile(buffer.getvalue(), name=f"{barcode_value}.png")
