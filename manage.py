#!/usr/bin/env python
import os
import sys
sys.path.append("{}/src".format(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_make_sqlalchemy_test.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
