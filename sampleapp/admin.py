from django.contrib import admin

import models

from django.db.models.base import ModelBase


for name, cls in models.__dict__.items():
    if isinstance(cls, ModelBase) and cls._meta.abstract is False:
        admin.site.register(cls)
