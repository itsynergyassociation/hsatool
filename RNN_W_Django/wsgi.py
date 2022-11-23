"""
WSGI config for RNN_W_Django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RNN_W_Django.settings')

application = get_wsgi_application()
from django_forest import init_forest
init_forest()
