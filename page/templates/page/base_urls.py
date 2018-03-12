from django.conf.urls import url

import views

urlpatterns = [{% for page in pages %}
    url(r'^{{page.url_pattern}}$',
        getattr(views.{{page.name}}, 'as_view')(),
        name='{{page.url_name}}'),{% endfor %}
]