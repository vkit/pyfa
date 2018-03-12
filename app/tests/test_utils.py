import os

from django.test import TestCase

from app.utils import startapp

from pyfactory_cnc.settings.base import PROJECT_APPS_DIR


class StartAppTest(TestCase):

    def setUp(self):
        self.app_code_name = 'startapp_test_app'
        startapp(self.app_code_name)

    def tearDown(self):
        is_deleted = os.system(
            "rm -r {0}/{1}".format(
                PROJECT_APPS_DIR,
                self.app_code_name)
        )
        self.assertEquals(is_deleted, 0)

    def test_start_app(self):
        is_file = os.path.isfile(
            '{0}/{1}/models.py'.format(
                PROJECT_APPS_DIR, self.app_code_name))
        self.assertTrue(is_file)

