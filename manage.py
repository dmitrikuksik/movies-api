#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    if os.environ.get('DJANGO_SETTINGS_MODE', '') == 'DOCKER':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_movies.settings_docker')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_movies.settings_dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
