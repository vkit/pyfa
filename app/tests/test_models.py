import os
from django.test import TestCase

from app.factories import AppFactory
from pyfactory_cnc.settings.base import PROJECT_APPS_DIR


class AppModelTest(TestCase):

    def setUp(self):
        self.app = AppFactory()

    def test_source_code_available(self):
        self.assertFalse(
            self.app.source_code_available()
        )

    def test_generate_codes(self):
        self.app.generate_codes()
        self.assertTrue(
            self.app.source_code_available()
        )
        os.system(
            "rm -r {0}/{1}".format(
                PROJECT_APPS_DIR,
                self.app.name)
        )
