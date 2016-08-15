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


class C(object):
    def __init__(self, v, start=None, end=None):
        self.v = v
        if start is None:
            if "\n" in self.v:
                self.start = '"""'
            else:
                self.start = '"'
        else:
            self.start = start
        if end is None:
            if "\n" in self.v:
                self.end = '"""'
            else:
                self.end = '"'
        else:
            self.end = end

    def __str__(self):
        return '{}{}{}'.format(self.start, self.v, self.end)

class CallCallable(object):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = list(args)  # type: list
        self.kwargs = kwargs  # type: dict

    def __str__(self):
        assert isinstance(self.name, str)
        paras = []
        for arg in self.args:
            paras.append(str(arg))
        for k, v in self.kwargs.items():
            paras.append("{}={}".format(k, str(v)))
        return "{}({})".format(self.name, ", ".join(paras))

class BindName(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        if isinstance(self.name, str):
            return "{} = {}".format(self.name, str(self.value))
        else:
            return "{} = {}".format(", ".join(self.name), str(self.value))

class TransferField(object):
    def __init__(self, field):
        assert isinstance(field, models.Field)
        self.field = field
        self.attrname, self.col_name = field.get_attname_column()
        self.bn = lambda v: BindName(self.field.get_attname(), v)

    def trans_col_name(self, field):
        attname, col_name = field.get_attname_column()
        if col_name is not None and attname != col_name:
            return col_name

    def trans_related(self, field):
        if isinstance(field, models.OneToOneField):
            print(field.rel.to._meta.object_name, field.rel.related_name, field.rel.related_query_name)
            warnings.warn(field)
        elif isinstance(field, models.ForeignKey):
            # print(field.rel.to._meta.object_name, field.rel.related_name, field.rel.related_query_name)
            rel_field_name = self.attrname[:-3] if self.attrname.endswith("_id") else self.attrname
            rel_field_id = "{}_id".format(rel_field_name)
            rel_field_attr_name, rel_field_db_name = field.rel.to._meta.pk.get_attname_column()
            yield BindName(rel_field_id, (CallCallable(
                "Column",
                "Interger",
                CallCallable(
                    "ForeignKey",
                    C("{}.{}".format(field.rel.to._meta.db_table, rel_field_db_name))
                )
            )))
            yield BindName(rel_field_name, CallCallable(
                "relationship",
                '"{}"'.format(field.rel.to._meta.object_name),
                back_populates=C("{}_set".format(rel_field_name))
            ))
        elif isinstance(field, models.ManyToManyField):
            warnings.warn(field)

    def trans_char(self, field):
        kwargs = self.trans_args(field)
        if field.max_length is not None:
            sa_type = CallCallable("String", field.max_length)
        else:
            sa_type = "String"
        return CallCallable("Column", sa_type, **kwargs)

    def trans_int(self, field):
        return CallCallable("Column", "Integer", **self.trans_args(field))

    def trans_args(self, field):
        kwargs = {}
        if field.null is not None:
            kwargs["nullable"] = field.null
        if field.primary_key:
            kwargs["primary_key"] = field.primary_key
        if field.default is not django_fields.NOT_PROVIDED:
            kwargs["default"] = field.default
        return kwargs

    def iter_trans(self):
        bn = self.bn
        field =self.field
        cls = self.field.__class__
        if cls in (
                models.ManyToManyField,
                models.OneToOneField,
                models.ForeignKey):
            for code in self.trans_related(field):
                yield code
        elif cls in (
                models.CharField,
                models.URLField,
                models.EmailField,
                models.SlugField):
            yield bn(self.trans_char(field))
        elif cls in (
                models.IntegerField,
                models.BigIntegerField,
                models.SmallIntegerField,
                models.PositiveSmallIntegerField,
                models.PositiveIntegerField):
            yield bn(self.trans_int(field))
        elif cls in (models.FileField, models.FilePathField):
            yield bn(self.trans_char(field))
        elif cls == models.AutoField:
            yield bn(CallCallable("Column", "Integer", **self.trans_args(field)))
        elif cls == models.BooleanField:
            yield bn(CallCallable("Column", "Boolean", **self.trans_args(field)))
        elif cls == models.TextField:
            yield bn(CallCallable("Column", "Text", **self.trans_args(field)))
        elif cls == models.DateTimeField:
            code = CallCallable("Column", "Datetime", **self.trans_args(field))
        elif cls == models.TimeField:
            yield bn(CallCallable("Column", "Time", **self.trans_args(field)))
        elif cls == models.DateField:
            yield bn(CallCallable("Column", "Data", **self.trans_args(field)))
        else:
            warnings.warn(self.field)

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
        self._many_to_many_tmp = []
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
        print ("\n".join(self.iter_format_code(code_struct)))
        return ("\n".join(self.iter_format_code(code_struct)))


    def field_to_sqlalchemy_class_code(self, field):
        assert isinstance(field, models.Field)
        tf = TransferField(field)
        for code in tf.iter_trans():
            yield code

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
            for code in self.field_to_sqlalchemy_class_code(field):
                sa_fields.append(code)
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


