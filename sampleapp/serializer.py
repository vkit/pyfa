from django.db.models.base import ModelBase

import models

from rest_framework import serializers


for name, cls in models.__dict__.items():
    if isinstance(cls, ModelBase) and cls._meta.abstract is False:
        Meta = type(
            'Meta',
            (object,),
            {
                'model': cls,
                'fields': '__all__'
            }
        )
        serializer_name = '{0}Serializer'.format(name)
        locals()[serializer_name] = type(
            serializer_name,
            (serializers.ModelSerializer,),
            {
                'Meta': Meta,
            }
        )
