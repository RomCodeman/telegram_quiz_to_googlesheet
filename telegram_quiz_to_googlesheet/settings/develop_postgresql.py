from telegram_quiz_to_googlesheet.settings.base import *
import django_on_heroku

django_on_heroku.settings(locals())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', None)
if DEBUG is None:
    DEBUG = False
else:
    if 'true' == DEBUG.lower():
        DEBUG = True
    else:
        DEBUG = False


ALLOWED_HOSTS = ["*"]
