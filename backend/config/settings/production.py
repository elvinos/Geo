from config.settings.base import *
import environ
env = environ.Env()
print("PRODUCTION SETTINGS")
DEBUG=False
SENTRY_DSN = env.str('SENTRY_DSN')
RAVEN_CONFIG = {
    'DSN': SENTRY_DSN
}

# Sentry Configuration
