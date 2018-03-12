import unittest
from django.test import RequestFactory
from django.contrib.auth.models import User

from base.views import GenericDataGridView


class GenericDataGridViewTest(unittest.TestCase):

    def test_get(self):

        # Setup request and view.
        request = RequestFactory().get('/fake-path')
        view = GenericDataGridView.as_view(
            list_display=['username'],
            model=User,
            template_name='base/for_testing/testing_template.html')
        # Run.
        response = view(request)
        self.assertEquals(
            response.template_name,
            ['base/for_testing/testing_template.html']
        )
        self.assertEquals(
            response.context_data['list_display'],
            ['username']
        )
        self.assertEquals(
            response.context_data['title'],
            ''
        )
        self.assertFalse(
            response.context_data['action']
        )
        self.assertTrue(
            response.context_data['check_box']
        )
        self.assertFalse(
            response.context_data['date_range']
        )
