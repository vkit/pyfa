from django.conf.urls import url

from .models import *

import views

urlpatterns = [
    # Project deatil or list of app for specific project.
    url(r'^$',
        views.PageListView.as_view(),
        name='index'),
    url(r'^create/$',
        views.PageCreateView.as_view(),
        name='create'),
]
