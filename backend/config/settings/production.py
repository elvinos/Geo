from config.settings.base import *
import environ
env = environ.Env()
print("PRODUCTION SETTINGS")
DEBUG=False
# ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '3.17.71.200', 'ec2-3-17-71-200.us-east-2.compute.amazonaws.com']
# ALLOWED_HOSTS =  ['localhost', '127.0.0.1']
print(ALLOWED_HOSTS)

# DOMAIN = env.str('http://localhost:8080')


# DEBUG= False
# ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', 'localhost', env.str('IP'), env.str('HOST_PROD'), 'backend']
# ALLOWED_HOSTS = ['*']

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
