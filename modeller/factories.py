import factory

# from django.contrib.auth.models import User

from factory.django import DjangoModelFactory

from .models import ModelField, ModelObject
from app.factories import AppFactory


class ModelObjectFactory(DjangoModelFactory):
    class Meta:
        model = ModelObject
    app = factory.SubFactory(AppFactory)
    name = "test_model"


class ModelFieldFactory(DjangoModelFactory):
    class Meta:
        model = ModelField
    model_obj = factory.SubFactory(ModelObjectFactory)
    name = "test_char"
    field_type = 9
    blank = False
    null = False
