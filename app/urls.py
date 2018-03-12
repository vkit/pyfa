from django.conf.urls import url

from .models import *

import views

urlpatterns = [
    # Project deatil or list of app for specific project.
    url(r'^$',
        views.AppListView.as_view(),
        name='index'),
    # Creates new App Obj
    url(r'^create/$',
        views.AppCreateView.as_view(),
        name='create'),
    # Keep urls with uuid below this
    # App detail page
    url(r'^(?P<pk>[^/]+)/$',
        views.AppDetailView.as_view(),
        name='detail'),
]
