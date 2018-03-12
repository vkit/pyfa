from django.conf.urls import url

from .models import *

import views

urlpatterns = [
    url(r'^create/$',
        views.ModelObjectCreateView.as_view(),
        name='create'),
    url(r'^create_field/$',
        views.ModelFieldCreateView.as_view(),
        name='create_field'),
    # modelobject deatil or list of modelfields for specific modelobject.
    url(r'^(?P<pk>[^/]+)/$',
        views.ModelObjectDetailView.as_view(),
        name='detail'),
]
