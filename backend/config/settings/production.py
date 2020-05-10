import environ
env = environ.Env()
print("PRODUCTION SETTINGS")
DEBUG= False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
# DOMAIN = env.str('HOST_PROD')

from config.settings.base import *

# import django_heroku
# INSTALLED_APPS.extend(["whitenoise.runserver_nostatic"])
#
# # Must insert after SecurityMiddleware, which is first in settings/common.py
# MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
#
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
#
# TEMPLATES[0]["DIRS"] = [os.path.join(ROOT_DIR, "../", "frontend", "dist")]
#
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# # STATICFILES_DIRS = [os.path.join(ROOT_DIR, "../", "frontend", "dist", "static")]
# WHITENOISE_ROOT = os.path.join(ROOT_DIR, "../", "frontend", "dist", "root")

# DATABASES['default'] =  dj_database_url.config()
# django_heroku.settings(locals())
