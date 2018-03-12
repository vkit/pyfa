"""pyfactory_cnc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os
from django.conf.urls import url, include
from django.contrib import admin

from pyfactory_cnc.settings.base import PROJECT_APPS_DIR

urlpatterns = [
    url(r'^', include('core.urls', namespace='core')),
    url(r'^admin/', admin.site.urls),
    url(r'^apps/', include('app.urls', namespace='app')),
    url(r'^pages/', include('page.urls', namespace='page')),
    url(r'^modeller/', include('modeller.urls', namespace='modeller')),
    url(
        r'^authentication/',
        include('authentication.urls', namespace='authentication')),
]

for item in os.listdir(PROJECT_APPS_DIR):
    if os.path.isfile(os.path.join(PROJECT_APPS_DIR, item, '__init__.py')):
        app_name = '%s' % item
        u = url(
            r'^{0}/'.format(app_name),
            include(
                '{0}.urls'.format(app_name),
                namespace='{0}'.format(app_name)
            )
        )
        if u not in urlpatterns:
            urlpatterns.append(u)
