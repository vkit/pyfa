# import factory

# from django.contrib.auth.models import User

from factory.django import DjangoModelFactory

from .models import App


class AppFactory(DjangoModelFactory):
    class Meta:
        model = App
    name = 'test_app'
