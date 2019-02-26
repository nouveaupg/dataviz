# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import AppealReceiptsData

# Register your models here.


class AppealReceiptsAdmin(admin.ModelAdmin):
    pass


admin.site.register(AppealReceiptsData, AppealReceiptsAdmin)
