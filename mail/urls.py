from django.conf.urls import url

from mail import views

urlpatterns = [
    url(r'^email/$', views.EmailView.as_view(),
        name='email'),
]
