# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand, CommandError
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
        for inst_app in settings.INSTALLED_APPS:
            print(inst_app)