from django.db import models



class A(models.Model):
    char = models.CharField("test char", max_length=128, null=True, blank=True)
    int = models.IntegerField("test", auto_created=True)
    test = models.ForeignKey("C", related_name="test_a")

    class Meta:
        verbose_name = "A"
        verbose_name_plural = "A"

class B(models.Model):
    text = models.TextField("text", null=True)
    a = models.BooleanField("bool", default=True)
    b = models.DateField("date", auto_now_add=True)

    class Meta:
        verbose_name = "B"
        abstract = True
        index_together = (
            ('a', "b"),
        )

class C(B):
    c = models.FileField("file")
    url = models.URLField('url')

    class Meta:
        unique_together = (
            ("b", "c"),
        )
