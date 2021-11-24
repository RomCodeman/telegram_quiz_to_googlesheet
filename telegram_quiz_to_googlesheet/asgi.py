"""
ASGI config for telegram_quiz_to_googlesheet project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_quiz_to_googlesheet.settings.develop_postgresql')

application = get_asgi_application()
