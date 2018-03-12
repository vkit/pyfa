from django.conf.urls import url

from base.views import GenericDynamicEditFormView

urlpatterns = [
    url(r'^edit_form/$', GenericDynamicEditFormView.as_view(),
        name='edit_form'),
]
