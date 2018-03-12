from django.contrib.auth.models import Group

from django.views.generic import TemplateView, ListView

from django.shortcuts import HttpResponseRedirect

from base.views import GenericDataGridView, GenericModalCreateView, BaseDeleteView
from base.mixin import GeneralContextMixin

from .models import BaseTemplate, Tab, SubTab
from .forms import BaseTemplateForm, GroupForm, SubTabForm, TabForm

from authentication.utils import codify_auth


class BaseTemplateListView(GeneralContextMixin, ListView):

    template_name = "authentication/index.html"
    context_object_name = 'base_templates'
    model = BaseTemplate

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateListView, self).get_context_data(**kwargs)
        context['form'] = BaseTemplateForm
        context['form_tab'] = TabForm
        context['form_subtab'] = SubTabForm
        return context


class BaseTemplateDetailView(GeneralContextMixin, TemplateView):

    template_name = "authentication/detail.html"


class GroupListView(GeneralContextMixin, GenericDataGridView):

    model = Group
    template_name = "authentication/group_index.html"
    list_display = (
        ('Name', 'name'),
        ('Permissions', 'permissions.all'),
    )

    sub_title = ''
    title = 'List Of Group'
    date_range = False
    check_box = False
    # detail_url_reverse = 'modeller:detail'

    def make_query(self, **kwargs):
        return self.model.objects.all()

    def make_date_query(self, request, raw_query, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['form'] = GroupForm
        return context


class GroupCreateView(GenericModalCreateView):

    form_class = GroupForm
    object_name = 'Group'
    success_url = '/authentication/groups'


class BaseTemplateCreateView(GenericModalCreateView):

    form_class = BaseTemplateForm
    object_name = 'Authentication Level'
    success_url = '/authentication/'


class TabCreateView(GenericModalCreateView):

    form_class = TabForm
    object_name = 'Tab'
    success_url = '/authentication/'

    def form_valid(self, form):
        instance = form.instance
        instance.base_template = BaseTemplate.objects.get(
            pk=self.request.POST.get('base_template'))
        return super(TabCreateView, self).form_valid(form)


class SubTabCreateView(GenericModalCreateView):

    form_class = SubTabForm
    object_name = 'SubTab'
    success_url = '/authentication/'

    def form_valid(self, form):
        instance = form.instance
        instance.tab = Tab.objects.get(
            pk=self.request.POST.get('tab'))
        return super(SubTabCreateView, self).form_valid(form)


class DeleteTabView(BaseDeleteView):
    permission_required = 'authentication.add_tab'
    model = Tab
    success_url = '/authentication/'


class DeleteSubTabView(BaseDeleteView):
    permission_required = 'authentication.add_tab'
    model = SubTab
    success_url = '/authentication/'


def update_base_template(request, pk):
    print pk
    t = BaseTemplate.objects.get(pk=pk)
    t.build_auth()
    return HttpResponseRedirect("/authentication/")


def update_authentication(request):
    """
    Creates/updates view and url files of core app"""
    codify_auth(file_name="views.py")
    codify_auth(file_name="urls.py")
    return HttpResponseRedirect("/authentication/")
