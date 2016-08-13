from django.test import TestCase
from django.core.management import call_command
# Create your tests here.


class ExportSqlAlchemyTestCase(TestCase):

    def test_call(self):
        res = call_command('export_sqlalchemy')
