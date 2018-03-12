from __future__ import unicode_literals
import os

from django.db import models

from pyfactory_cnc.settings.base import PROJECT_APPS_DIR

from base.models import TimeStamp
from modeller.models import ModelObject
from page.models import Page

from .utils import startapp, makemigrations, migrate, codify

import logging
logger = logging.getLogger(__name__)


class App(TimeStamp):

    name = models.SlugField(max_length=50, unique=True, blank=False)

    def __unicode__(self):
        return self.name

    def code_name(self):
        return self.name.lower()

    def total_models(self):
        return self.modelobject_set.count()

    def source_code_available(self):
        """
        """
        return os.path.isfile(
            "{0}/{1}/views.py".format(
                PROJECT_APPS_DIR, self.code_name()))

    def generate_codes(self, *args, **kwargs):
        """
        Generates source codes, this method is
        equivalent to django startapp command.
        See startapp().
        """
        if not self.source_code_available():
            startapp(self.code_name())
            return True
        else:
            return False

    def write_models(self):
        codify(
            app_name=self.code_name(),
            template='modeller/base_models.py',
            file='models',
            model_objects=ModelObject.objects.filter(app=self))
        # Writes an empty file in methods folder
        model_list = list()
        for model in self.modelobject_set.all():
            model_list.append(model.name.lower())
            file = os.path.isfile('{1}/{0}/methods/{2}.py'.format(
                self.code_name(),
                PROJECT_APPS_DIR,
                model.name.lower()
            )
            )
            if not file:
                model_file = open(
                    '{1}/{0}/methods/{2}.py'.format(
                        self.code_name(),
                        PROJECT_APPS_DIR,
                        model.name.lower()),
                    'w')
                model_file.write('')
                model_file.close()
        # Writes import in __init__ file of methods folder
        init_file = open(
            '{1}/{0}/methods/__init__.py'.format(
                self.code_name(),
                PROJECT_APPS_DIR),
            'w')
        imports = ','.join(model_list)
        init_file.write('import {0}'.format(imports))
        init_file.close()
        return True

    def migrate(self):
        migrate(self.code_name())

    def makemigrations(self):
        makemigrations(self.code_name())

    def write_pages(self):
        """
        Writes/updates view and url file of an app
        using all the Page objects under it
        """
        pages = Page.objects.filter(app=self)
        codify(
            app_name=self.code_name(),
            pages=pages,
            template='page/base_pages.py',
            file='views'
        )
        codify(
            app_name=self.code_name(),
            pages=pages,
            template='page/base_urls.py',
            file='urls'
        )
