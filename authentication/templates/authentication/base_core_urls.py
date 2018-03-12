"""standardmodel url"""
from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$',
        'django.contrib.auth.views.login',
        {'template_name': 'signin.html'}),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'template_name': 'signin.html'}, name='logout'),
    url(r'^standardmodel/$',
        DashboardStandModView.as_view(), name='standardmodel'),
    url(r'^dashboard_dispatcher/$',
        DashboardDispatcherView.as_view(), name='dashboard_dispatcher')
]

{% for template in base_templates %}
{% if template.templatified %}
urlpatterns.append(
    url(r'^{{template.dashboard_url}}$',
        getattr({{template.dashboard_view_name}}, 'as_view')(),
        name='{{template.dashboard_url}}')
    ){% endif %}{% endfor %}