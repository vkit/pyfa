from django.conf.urls import url

from .models import *

import views

urlpatterns = [
    url(r'^$',
        views.BaseTemplateListView.as_view(),
        name='index'),
    url(r'^create_tab/$',
        views.TabCreateView.as_view(),
        name='create_tab'),
    url(r'^create_subtab/$',
        views.SubTabCreateView.as_view(),
        name='create_subtab'),
    url(r'^groups/$',
        views.GroupListView.as_view(),
        name='groups'),
    url(r'^update_auth/$',
        views.update_authentication,
        name='update_auth'),
    url(r'^create_group/$',
        views.GroupCreateView.as_view(),
        name='create_group'),
    url(r'^create_authentication_level/$',
        views.BaseTemplateCreateView.as_view(),
        name='create_authentication_level'),
    url(r'^(?P<pk>[^/]+)/$',
        views.BaseTemplateDetailView.as_view(),
        name='detail'),
    url(r'^(?P<pk>[^/]+)/update_base_template$',
        views.update_base_template,
        name='update_base_template'),
    url(r'^(?P<pk>[^/]+)/delete_tab/$',
        views.DeleteTabView.as_view(),
        name='delete_tab'),
    url(r'^(?P<pk>[^/]+)/delete_subtab/$',
        views.DeleteSubTabView.as_view(),
        name='delete_subtab'),
]
