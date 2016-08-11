# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import models
import django
from django.conf import settings

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            type=str,
            nargs='?',
            default=os.path.abspath(os.path.join(os.path.curdir, "sqlalchemy"))
        )
        parser.add_argument('-a', '--app', nargs='*', type=str)


    def handle(self, *args, **options):
        print(args, options)
        self.load_models(options['app'])


    def load_models(self, apps=None):
        if django.VERSION[1] > 7 :
            from django.apps import apps
            for inst_app in settings.INSTALLED_APPS:
                app_models = apps.get_app_config(inst_app).get_models()
                print(app_models)
        else:
            from django.db import models
            models.get_models(include_auto_created=True)
        return