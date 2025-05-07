import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile

# Utility function to generate barcode images for items and board stock
# Supports CODE128 by default, which is widely used for warehouse management
# Returns a Django ContentFile object, ready for saving to a model ImageField

def generate_barcode_image(barcode_value, file_format="PNG", barcode_type="code128", write_text=False, text_distance=5):
    # Get the correct barcode class (e.g., CODE128, EAN13)
    CODE_CLASS = barcode.get_barcode_class(barcode_type)
    buffer = BytesIO()
    barcode_obj = CODE_CLASS(barcode_value, writer=ImageWriter())
    # Generate the barcode image and write it to the buffer
    barcode_obj.write(buffer, options={
        'write_text': write_text,  # Include the human-readable text below the barcode
        'text_distance': text_distance,  # Distance of text from the barcode
        'module_width': 0.4,  # Width of each barcode bar
        'module_height': 15,  # Height of the barcode
        'font_size': 10,  # Size of the text (if enabled)
    })
    # Return the image as a Django ContentFile
    return ContentFile(buffer.getvalue(), name=f"{barcode_value}.{file_format.lower()}")
