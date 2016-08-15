# -*- coding: utf-8 -*-
import os
import warnings
import django
from django.utils import six
from django.db.models import fields as django_fields
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.apps import apps
from collections import OrderedDict


class Command(BaseCommand):
    _function_list = None  # save callbeck function
    BASE_CLASS_NAME = "base"

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
        if not options['app']: options['app'] = None  # django 1.7 optarg don't have arguments app is empty list
        self._function_list = []
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
            if django.VERSION[1] > 7:
                from django.apps import apps as django_apps
                iter_models = django_apps.get_models()
            else:
                from django.db import models
                # include_auto_created parameter ensures that through tables implicitly
                # created by ManyToManyFields will be retrieved as well.
                iter_models = models.get_models(include_auto_created=True)
            for model in iter_models:
                yield model
        else:
            for app in apps:
                for model in self.app_str_to_app_config(app).get_models():
                    yield model

    def iter_fields(self, model):
        fields_iter = iter(model._meta.concrete_fields)
        for field in fields_iter:
            yield field

    def load_models(self, apps=None):
        res = OrderedDict()
        code_struct = []
        for model in self.iter_models(apps):
            code_struct.extend(self.model_to_sqlalchemy_class_code(model))
            code_struct.extend(['', ''])

        print("\n".join(self.iter_format_code(code_struct)))


    def field_to_sqlclchemy_type(self, field):
        """
        transfer rule:
        sqlalchemy Type:
            String
                Text
                Unicode
                UnicodeText
                Enum
            Integer
                SmallInteger
                BigInteger
            Numeric
                Float
            DateTime
            Date
            Time
            LargeBinary
                Binary
            Boolean
            Interval
        django Type
            AutoField
            BooleanField                    ->  Boolean
            CharField                       ->  String, Enum
                EmailField                  ->  String
                SlugField                   ->  String
                URLField                    ->  String
            FileField                       ->  String
            FilePathField                   ->  String
            TextField                       ->  Text
            CommaSeparatedIntegerField      ->  Text
            DateField                       ->  Date
                DateTimeField               ->  DateTime
            TimeField                       ->  Time
            DecimalField                    ->  Numeric
            DurationField                   ->  Interval
            FloatField                      ->  Float
            IntegerField                    ->  Integer
                BigIntegerField             ->  BigInteger
                SmallIntegerField           ->  SmallInteger
                PositiveIntegerField
                PositiveSmallIntegerField
            IPAddressField
            GenericIPAddressField
            NullBooleanField
            BinaryField
            UUIDField

        :param field:
        :return: ( sqlalchemy type name , {key :args, ...} )
        """
        assert isinstance(field, models.Field)
        sa_type = {
            models.ManyToManyField:     (self.trans_related(field),),
            models.ForeignKey:          (self.trans_related(field),),
            models.OneToOneField:       (self.trans_related(field),),
            models.AutoField:           (("Column", "Integer"), self.trans_args(field)),
            models.BooleanField:        (("Column", "Boolean"), self.trans_args(field)),
            models.CharField:           (self.trans_char(field), self.trans_args(field)),
                models.URLField:            (self.trans_char(field), self.trans_args(field)),
                models.EmailField:          (self.trans_char(field), self.trans_args(field)),
                models.SlugField:           (self.trans_char(field), self.trans_args(field)),
            models.TextField:           (("Column", "Text"), self.trans_args(field)),
            models.IntegerField:        (self.trans_int(field), self.trans_args(field)),
                models.BigIntegerField: (self.trans_int(field), self.trans_args(field)),
                models.SmallIntegerField: (self.trans_int(field), self.trans_args(field)),
                models.PositiveSmallIntegerField: (self.trans_int(field), self.trans_args(field)),
                models.PositiveIntegerField: (self.trans_int(field), self.trans_args(field)),
            models.FileField:           (self.trans_char(field), self.trans_args(field)),
            models.FilePathField:       (self.trans_char(field), self.trans_args(field)),
            models.DateTimeField:       (("Column", "Datetime"), self.trans_args(field)),
            models.TimeField:           (("Column", "Time"), self.trans_args(field)),
            models.DateField:           (("Column", "Data"), self.trans_args(field)),
        }.get(field.__class__, type(field))
        return sa_type

    def trans_related(self, field):
        if field.many_to_many:
            print(field.remote_field)
        return "relationship",

    def trans_char(self, field):
        if field.max_length is not None:
            sa_type = "String({})".format(field.max_length)
        else:
            sa_type = "String"
        return "Column", sa_type

    def trans_int(self, field):
        return "Column", "Integer"

    def trans_args(self, field):
        kwargs = {}
        if field.null is not None:
            kwargs["nullable"] = field.null
        if field.primary_key:
            kwargs["primary_key"] = field.primary_key
        if field.default is not django_fields.NOT_PROVIDED:
            kwargs["default"] = field.default
        return kwargs

    def field_to_sqlalchemy_class_code(self, field, attname):
        assert isinstance(field, models.Field)

        rule = (self.field_to_sqlclchemy_type(field))
        para_list = []
        args_str = ", ".join(rule[0][1:])
        if args_str:
            para_list.append(args_str)
        if len(rule) > 1:
            for k, v in rule[1].items():
                para_list.append("{}={}".format(k, v))

        return "{name} = {f_name}({args})".format(
            name=field.attname,
            f_name=rule[0][0],
            args=", ".join(para_list)
        )

    def model_to_sqlalchemy_class_code(self, model):
        sa_block = "class {class_name}({base_name}):".format(
            class_name=model._meta.object_name,
            base_name=self.BASE_CLASS_NAME
        )
        sa_fields = [
            '"""',
            'Auto transfer from django app `{}` by django_make_sqlalchemy'.format(model._meta.app_label),
            models.__doc__ if models.__doc__ else "",
            '"""',
            '__tablename__ = "{table_name}"'.format(table_name=model._meta.db_table),
        ]

        for field in self.iter_fields(model):
            sa_fields.append(self.field_to_sqlalchemy_class_code(field, field.attname))
        return [sa_block, sa_fields]

    def iter_format_code(self, code, level=0):
        for subcode in code:
            if isinstance(subcode, list):
                yield "\n".join(self.iter_format_code(subcode, level+1))
            else:
                indent = "    " * level
                if subcode:
                    yield ("{}{}".format(indent, subcode))
                else:
                    yield ("")


