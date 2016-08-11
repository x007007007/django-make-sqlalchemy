from django.test import TestCase
from .management.commands.export_sqlalchemy import Command
from django.core.management import call_command
# Create your tests here.

class ExportSqlAlchemyTestCase(TestCase):

    def test_1(self):
        res = call_command('export_sqlalchemy')
        print(res)