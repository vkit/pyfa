import collections
from django.contrib.auth.models import User, Permission, Group
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

from django.test.client import Client

compare = lambda x, y: collections.Counter(x) == collections.Counter(y)


class BaseTestMixin(object):
    """
    This mixin can be as base test for  urls and views.
    Required attributes:
    1) 'url' is url in django reverse format Ex:
        url = 'name_space:name'
    2) 'status_code' is HTTP status you are expecting

    Optional attributes:
    1) 'permission_required' is permission code name that user
        need to access the url.
        Ex:
        permission_codename = 'add_jobcard'
    2) 'list_context_variables' is dict whose keys are
        template context_variable(of list type)
        and values are the expected results
        Ex:
        list_context_variables = {'jobcard': Jocard.objects.all()}
    3) 'obj_context_variables' is dict whose keys are
        template_context variable(of single obj/form type) name
        and values are the expected results Ex:
        obj_context_variables = {
            'form': SomeForm,
            'jobcard': JobCard.object.get(pk=something)
            }
    """

    permission_codename = None
    url = None
    status_code = None
    list_context_variables = None
    args = None
    form_context_variables = None
    obj_context_variables = None

    def setUp(self):
        self.user = User.objects.create_user(
            'user', 'lennon@thebeatles.com', 'user')
        group = Group.objects.create(name='admin')
        self.user.groups.add(group)
        if self.permission_codename:
            self.user.user_permissions.add(
                Permission.objects.get(codename=self.permission_codename).id)
            self.user.save()
        self.client = Client()
        self.client.login(username='user', password='user')

    def test_view(self):
        if not self.url and self.status_code:
            raise ImproperlyConfigured(
                "BaseTestMixin requires either a definition of "
                "'url and status_code'")
        if self.args:
            print self.args
            response = self.client.get(reverse(
                self.url, args=self.args))
        else:
            response = self.client.get(reverse(self.url))
        self.assertEquals(response.status_code, self.status_code)
        if self.list_context_variables:
            for context, values in self.list_context_variables.items():
                self.assertTrue(
                    compare(response.context_data[context], values))
        if self.obj_context_variables:
            for context, values in self.obj_context_variables.items():
                self.assertEquals(
                    response.context_data[context], values)
        if self.form_context_variables:
            for context, values in self.form_context_variables.items():
                self.assertTrue(
                    isinstance(response.context_data[context], values))


class BaseModalCreateTestMixin(object):
    permission_codename = None
    url = None
    status_code = None
    model = None
    args = None

    def setUp(self):
        self.user = User.objects.create_user(
            'user', 'lennon@thebeatles.com', 'user')
        if self.permission_codename:
            self.user.user_permissions.add(
                Permission.objects.get(codename=self.permission_codename).id)
            self.user.save()
        return super(BaseModalCreateTestMixin, self).setUp()

    def test_modal_create_view(self):
        client = Client()
        client.login(username='user', password='user')
        if not self.url and self.status_code:
            raise ImproperlyConfigured(
                "BaseTestMixin requires either a definition of "
                "'url and status_code'")
        if self.args:
            response = client.post(
                reverse(self.url, args=self.args), self.payload)
        else:
            response = client.post(reverse(self.url), self.payload)
        self.assertEquals(response.status_code, self.status_code)
        self.assertEquals(self.model.objects.count(), 1)


class BaseTestModelMixin(object):
    model = None
    factory = None

    def setUp(self):
        self.factory = self.factory.create()

    def test_model_create(self):
        self.assertEqual(self.model.objects.count(), 1)
        self.assertTrue(isinstance(self.factory, self.model))
