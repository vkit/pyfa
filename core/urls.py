"""standardmodel url"""
from django.conf.urls import url
from .import views
from .views import *

urlpatterns = [
    url(r'^$',
        'django.contrib.auth.views.login',
        {'template_name': 'signin.html'}),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'template_name': 'signin.html'}, name='logout'),
    url(r'^dashboard_dispatcher/$',
        DashboardDispatcherView.as_view(), name='dashboard_dispatcher'),
    url(r'^standardmodel/$',
        DashboardStandModView.as_view(), name='standardmodel'),

    # For change password
    url(r'^change_password/', views.change_password, name='change_password'),
]


urlpatterns.append(
    url(r'^admin_dashboard/$',
        getattr(AdminDashboardView, 'as_view')(),
        name='admin_dashboard')
    )

urlpatterns.append(
    url(r'^operator_dashboard/$',
        getattr(OperatorDashboardView, 'as_view')(),
        name='operator_dashboard/')
    )