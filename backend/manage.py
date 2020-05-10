#!/usr/bin/env python
import os
import sys
import socket

if __name__ == '__main__':

#     ipaddress = socket.gethostbyname( socket.gethostname() )
#     print(ipaddress)
#     if ipaddress == '127.0.0.1':
#             settings = 'config.settings.development'
#             print("Development")
#     else:
#         settings = 'config.settings.production'
#         print("Production")

    settings = 'config.settings.production'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                """Couldn't import Django. Are you sure it's installed and
                   available on your PYTHONPATH environment variable? Did you
                   forget to activate a virtual environment?""",
            )
        raise

    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_path)
    sys.path.append(os.path.join(current_path, 'apps'))
    execute_from_command_line(sys.argv)
