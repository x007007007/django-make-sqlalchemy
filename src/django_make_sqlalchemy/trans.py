from django.db import models
from django_make_sqlalchemy.utils import lex as l


class SqlAlchemyModelClass(l.ClassStem):
    BASE_CLASS_NAME = "Base"

    def __init__(self, model):
        assert issubclass(model, models.Model)
        self.model = model
        self.stems = l.Stems()

    def get_lines(self):
        self.name = self.model._meta.object_name
        self.args = self.BASE_CLASS_NAME

        self.stems.append(
            l.Bind(__tablename__= self.model._meta.db_table)
        )

        for field in self.model._meta.concrete_fields:
            attrname, col_name = field.get_attname_column()


        for i in super(SqlAlchemyModelClass, self).get_lines(): yield i


