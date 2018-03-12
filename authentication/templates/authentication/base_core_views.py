from django.views.generic import TemplateView
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

from base.mixin import GeneralContextMixin


class DashboardDispatcherView(GeneralContextMixin, TemplateView):

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('auth.add_user'):
            return HttpResponseRedirect(reverse('standardmodel'))
        else:
            return HttpResponseRedirect('/admin/')


class DashboardStandModView(GeneralContextMixin, TemplateView):
    template_name = 'dashboard.html'


{% for template in base_templates %}
{% if template.templatified %}
locals()['{{template.dashboard_view_name}}'] = type(
    '{{template.dashboard_view_name}}',
    (GeneralContextMixin, TemplateView),
    {
        'template_name': 'project_base/{{template.file_name}}'
    }
)
{% endif %}
{% endfor %}
