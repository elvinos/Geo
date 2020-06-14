import environ
env = environ.Env()

print("DEVELOPMENT SETTINGS")

DEBUG = True
ALLOWED_HOSTS = ['*']
DOMAIN = env.str('LOCAL_DOMAIN')


from config.settings.base import *

SENTRY_DSN = ''
RAVEN_CONFIG = {
    'DSN': SENTRY_DSN
}