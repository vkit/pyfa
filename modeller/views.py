from django.shortcuts import HttpResponseRedirect

from base.views import (
    GenericDataGridView, GenericSelfRedirection, GenericModalCreateView
)
from base.mixin import GeneralContextMixin

from models import ModelField, ModelObject
from forms import ModelObjectForm, ModelFieldForm


class ModelObjectDetailView(GeneralContextMixin, GenericDataGridView):

    model = ModelField
    template_name = "modeller/detail.html"
    list_display = (
        ('Name', 'name'),
        ('Field type', 'get_field_type_display'),
        ('Is Null', 'null'),
        ('Is Blank', 'blank'),
        ('Created on', 'created_at'),
        ('Last updated', 'updated_at'),
    )
    # title = 'List Fields'
    sub_title = ''
    date_range = False
    detail_url_reverse = ''
    action_dict = {
        'Delete': "delete",
    }

    def make_query(self, **kwargs):
        # TO DO: Add 404 error
        return ModelField.objects.filter(model_obj=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(ModelObjectDetailView, self).get_context_data(**kwargs)
        context['form'] = ModelFieldForm
        context['model_obj'] = ModelObject.objects.get(
            pk=self.kwargs.get('pk'))
        context['title'] = 'List of field for {0} transaction'.format(
            context['model_obj'])
        return context

    def delete(self):
        objs = self.model.objects.filter(pk__in=self.for_action_keys)
        for obj in objs:
            obj.delete()
        return self.success_url()

    def success_url(self):
        return HttpResponseRedirect(self.request.META['PATH_INFO'])


class ModelObjectCreateView(GenericSelfRedirection):

    form_class = ModelObjectForm
    object_name = 'Transaction'
    url_pattern_list = ['modeller']

    def get_error_url(self):
        return '/apps/{0}'.format(self.request.POST['app'])


class ModelFieldCreateView(GenericModalCreateView):

    form_class = ModelFieldForm
    object_name = 'Field'

    def get_success_url(self):
        return '/modeller/{0}'.format(self.request.POST['model_obj'])

    def form_valid(self, form):
        instance = form.instance
        instance.model_obj = ModelObject.objects.get(
            pk=self.request.POST.get('model_obj'))
        return super(ModelFieldCreateView, self).form_valid(form)
