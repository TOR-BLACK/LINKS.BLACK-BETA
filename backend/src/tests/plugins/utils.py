from django.conf import settings
from django.core.files.base import File

import io
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def generate_translate_field_value(field_name, value) -> dict:
    data = {
        field_name: value
    }
    for lang, _ in settings.LANGUAGES:
        data[f'{field_name}_{lang}'] = value
    return data


def get_test_file(filename='test_file.txt'):
    file = io.BytesIO(b'Test file content')
    uploaded_file = SimpleUploadedFile(
        name=filename,
        content=file.read(),
        content_type='text/plain'
    )
    return uploaded_file


def get_test_image(filename='test_image.png'):
    image = Image.new('RGB', (100, 100), color='blue')
    image_io = io.BytesIO()
    image.save(image_io, format='PNG')
    image_io.seek(0)
    uploaded_image = SimpleUploadedFile(
        name=filename,
        content=image_io.read(),
        content_type='image/png'
    )

    return uploaded_image
