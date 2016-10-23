from django.db import models


class ForeignKeyModel(models.Model):
    t_char = models.CharField("test char", max_length=128, null=True, blank=True, db_column="test_char")
    t_int = models.IntegerField("test", auto_created=True)
    t_test = models.ForeignKey("ManyToManyAAndUniqueTogether", related_name="test_a")

    class Meta:
        verbose_name = "A1"
        verbose_name_plural = "A1"


class AbstractAndIndexTogethor(models.Model):
    t_text = models.TextField("text", null=True)
    t_bool = models.BooleanField("bool", default=True)
    t_date = models.DateField("date", auto_now_add=True)

    class Meta:
        verbose_name = "B"
        abstract = True
        index_together = (
            ('t_bool', "t_text"),
        )


class ManyToManyAAndUniqueTogether(AbstractAndIndexTogethor):
    t_file = models.FileField("file")
    t_url = models.URLField('url')
    t_datetime = models.DateTimeField(auto_now=True)
    b_side = models.ManyToManyField("ManyToManyBAndOneTOOneA", through="ManyToMany_rel")

    class Meta:
        unique_together = (
            ("t_file", "t_url"),
        )


class ManyToManyBAndOneToOneA(models.Model):
    a_side = models.ManyToManyField("ManyToManyAAndUniqueTogether", through="ManyToMany_rel")
    b_side = models.OneToOneField("OneToOneB")


class OneToOneB(models.Model):
    a_side = models.OneToOneField("ManyToManyBAndOneToOneA")


class ManyToMany_rel(models.Model):
    a = models.ForeignKey("ManyToManyAAndUniqueTogether")
    b = models.ForeignKey("ManyToManyBAndOneTOOneA")