# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import models
import django
from django.conf import settings
from django.utils.module_loading import import_module
from django.apps import apps
import warnings






class Command(BaseCommand):
    if django.VERSION[1] == 7:
        from optparse import make_option
        def _opt_callback(option, opt, value, parser, *args, **kwargs):
            if not hasattr(parser.values, 'app'):
                parser.values._update_loose({
                    "app": []
                })
            if isinstance(parser.values.app, list):
                parser.values.app.append(value)
            else:
                parser.values._update_loose({
                    "app": [value]
                })
        option_list = BaseCommand.option_list + (
            make_option(
                '-p', '--path',
                type=str,
                nargs=1,
                default=os.path.abspath(os.path.join(os.path.curdir, "sqlalchemy")),
                help='set out put directory',
            ),
            make_option(
                '-a', '--app',
                action="callback",
                callback=_opt_callback,
                default=[],
                type=str,
                help='select export app'
            )
        )
    else:
        def add_arguments(self, parser):
            parser.add_argument(
                'path',
                type=str,
                nargs='?',
                default=os.path.abspath(os.path.join(os.path.curdir, "sqlalchemy"))
            )
            parser.add_argument('-a', '--app', nargs='*', type=str)

    help = 'Closes the specified poll for voting'


    def handle(self, *args, **options):
        self.load_models(options["app"])

    @staticmethod
    def app_str_to_app_config(app_id):  #  type: django.apps.config.AppConfig
        """

        :param app_id: app label or app module __name__
        :return: AppConfig
        :rtype: django.apps.config.AppConfig
        """
        if app_id in apps.app_configs:
            return apps.app_configs[app_id]
        else:
            raise CommandError("can't find app `{}`".format(app_id))


    def iter_models(self, apps=None):
        if apps is None:
            pass
        else:
            for app in apps:
                for models in self.app_str_to_app_config(app).get_models():
                    yield models


    def load_models(self, apps=None):
        for models in self.iter_models(apps):
            print(models)
