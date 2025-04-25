import os
from django.conf import settings

def get_wkhtmltopdf_path():
    return os.path.join(settings.BASE_DIR, 'bin', 'wkhtmltopdf.exe')
