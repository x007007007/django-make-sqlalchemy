from django.contrib import admin
from .models import *


class Admin(admin.ModelAdmin):
    pass


admin.site.register(A, Admin)
admin.site.register(C, Admin)