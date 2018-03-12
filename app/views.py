from django.contrib import messages

from django.shortcuts import HttpResponseRedirect

from base.views import (
    GenericDataGridView, GenericSelfRedirection, GenericMultiDataGridView)
from base.mixin import GeneralContextMixin

from models import App
from forms import AppForm

from modeller.models import ModelObject
from modeller.forms import ModelObjectForm
from page.models import Page
from page.forms import PageForm


class AppListView(GeneralContextMixin, GenericDataGridView):

    model = App
    template_name = "app/index.html"
    list_display = (
        ('Name', 'name'),
        ('Models', 'total_models'),
        ('Source Code Available', 'source_code_available'),
        ('Created on', 'created_at'),
        ('Last updated', 'updated_at'),
    )
    title = 'List of Apps'
    sub_title = ''
    date_range = False
    detail_url_reverse = 'app:detail'
    action_dict = {
        "Generate Source code": 'generate_source_code',
        "Write models": 'write_models',
        'Make Migrations': 'makemigrations',
        'Migrate': 'migrate',
        'Write pages': 'write_pages',
    }

    def get_context_data(self, **kwargs):
        context = super(AppListView, self).get_context_data(**kwargs)
        context['form'] = AppForm
        return context

    def generate_source_code(self):
        apps = App.objects.filter(pk__in=self.for_action_keys)
        for app in apps:
            if not app.generate_codes():
                messages.error(
                    self.request,
                    "Source code for app {0} already generated".format(
                        app.name)
                )
        return self.success_url()

    def write_models(self):
        apps = App.objects.filter(pk__in=self.for_action_keys)
        for app in apps:
            app.write_models()
        return self.success_url()

    def migrate(self):
        apps = App.objects.filter(pk__in=self.for_action_keys)
        for app in apps:
            app.migrate()
        return self.success_url()

    def makemigrations(self):
        apps = App.objects.filter(pk__in=self.for_action_keys)
        for app in apps:
            app.makemigrations()
        return self.success_url()

    def write_pages(self):
        apps = App.objects.filter(pk__in=self.for_action_keys)
        for app in apps:
            app.write_pages()
        return self.success_url()

    def success_url(self):
        return HttpResponseRedirect(self.request.META['PATH_INFO'])


class AppCreateView(GenericSelfRedirection):

    form_class = AppForm
    object_name = 'App'
    error_url = '/apps/'
    url_pattern_list = ['apps']


class AppDetailView(GeneralContextMixin, GenericMultiDataGridView):

    template_name = "app/detail.html"
    list_display = (
        ('Name', 'name'),
        ('Created on', 'created_at'),
        ('Last updated', 'updated_at'),
    )

    model_matrix = [
        {
            'model_class': ModelObject,
            'list_display': (
                ('Name', 'name'),
                ('Total Fields', 'fields_count'),
                ('Created on', 'created_at'),
                ('Last updated', 'updated_at'),
            ),
            'title': 'List Transactions',
            'sub_title': '',
            'date_range': False,
            'detail_url_reverse': 'modeller:detail',
            'check_box': True,
            'action_dict': None,
            'edit': False,
            'query_method': 'model_object_query',
        },
        {
            'model_class': Page,
            'list_display': (
                ('Name', 'name'),
                ('App', 'app'),
                ('Transaction', 'model'),
                ('Url', 'url_pattern'),
                ('Type', 'get_page_type_display'),
                ('Created on', 'created_at'),
                ('Last updated', 'updated_at'),
            ),
            'title': 'List of Pages',
            'sub_title': '',
            'date_range': False,
            'detail_url_reverse': '',
            'check_box': True,
            'action_dict': None,
            'edit': False,
            'query_method': 'page_object_query',
        }
    ]

    sub_title = ''
    title = 'List Of Tranactions'
    date_range = False

    def model_object_query(self, **kwargs):
        return ModelObject.objects.filter(app=self.kwargs.get('pk'))

    def page_object_query(self, **kwargs):
        return Page.objects.filter(app=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(AppDetailView, self).get_context_data(**kwargs)
        context['model_object_form'] = ModelObjectForm
        context['app'] = App.objects.get(pk=self.kwargs.get('pk'))
        context['form_pages'] = PageForm
        return context
