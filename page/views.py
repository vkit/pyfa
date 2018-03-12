# from django.shortcuts import HttpResponseRedirect

from base.views import GenericDataGridView, GenericModalCreateView
from base.mixin import GeneralContextMixin

from .models import Page
from .forms import PageForm


class PageListView(GeneralContextMixin, GenericDataGridView):

    model = Page
    template_name = "page/index.html"
    list_display = (
        ('Name', 'name'),
        ('App', 'app'),
        ('Transaction', 'model'),
        ('Url', 'url_pattern'),
        ('Type', 'get_page_type_display'),
        ('Created on', 'created_at'),
        ('Last updated', 'updated_at'),
    )
    title = 'List of Pages'
    sub_title = ''
    date_range = False
    # detail_url_reverse = 'modeller:index'


class PageCreateView(GenericModalCreateView):

    form_class = PageForm
    object_name = 'Page'

    def get_success_url(self):
        return '/apps/{0}'.format(self.request.POST['app'])

    # def form_valid(self, form):
    #     instance = form.instance
    #     instance.model_obj = Page.objects.get(
    #         pk=self.request.POST.get('model_obj'))
    #     return super(PageCreateView, self).form_valid(form)
