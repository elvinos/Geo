import environ
env = environ.Env()
print("STAGING SETTINGS")
DEBUG= False
ALLOWED_HOSTS = '*'
# DOMAIN = env.str('HOST_PROD')

from config.settings.base import *