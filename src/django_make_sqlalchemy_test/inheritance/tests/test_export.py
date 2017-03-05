from django.test import TestCase
from django.core.management import call_command
# Create your tests here.
from django_make_sqlalchemy.trans import SqlAlchemyModelClass
from django_make_sqlalchemy_test.inheritance.models import ForeignKeyModel


class ExportSqlAlchemyTestCase(TestCase):

    def test_call(self):
        pass
        #res = call_command('export_sqlalchemy')

    def test_class(self):
        a = SqlAlchemyModelClass(ForeignKeyModel)
        print(a)