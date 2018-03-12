import os

from django.test import TestCase

from authentication.utils import templatify_auth

from pyfactory_cnc.settings.base import PROJECT_BASE_TEMPLATE_DIR


class TemplatifyTest(TestCase):

    def setUp(self):
        templatify_auth(
            base_template='base/master_base.html',
            file_name='sample.html'
        )

    def tearDown(self):
        is_deleted = os.system(
            "rm {0}/sample.html".format(PROJECT_BASE_TEMPLATE_DIR)
        )
        self.assertEquals(is_deleted, 0)

    def test_tempaltify(self):
        is_file = os.path.isfile(
            '{0}/sample.html'.format(PROJECT_BASE_TEMPLATE_DIR))
        self.assertTrue(is_file)
