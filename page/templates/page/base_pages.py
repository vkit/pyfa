from base.views import GenericDataGridView
from base.mixin import GeneralContextMixin

from .models import *

{% for page in pages %}
locals()["{{page.name}}"] = type(
    '{{page.name}}',
    ({{page.page_type}},),
    {
        'list_display': ({% for field in page.list_display.all %}
            ('{{field.name}}', '{{field.name}}'),{% endfor %}
        ),
        'template_name': 'page/base_index.html',
        'model': {{page.model.name}},
        'title': '{{page.title}}',
        'sub_title': '{{page.sub_title}}',
        'date_range': {{page.date_range}},
        'check_box': {{page.check_box}},
    }
)
{% endfor %}