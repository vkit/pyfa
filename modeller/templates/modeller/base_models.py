from __future__ import unicode_literals

from django.db import models

from base.models import TimeStamp, Contact
import methods

{% for model in model_objects %}


# {% for field in model.modelfield_set.all %}
# 	{% if field.choices %}
# 		{{field.name | upper}} = "{{field.choices}}"
# 	{% endif %}
# {% endfor %}

{{model.name}}Dict = {
    '__module__': '{{model.app.code_name}}',
{% for field in model.modelfield_set.all %}
    '{{field.name|lower}}': models.{{field.get_field_type_display}}({% include 'modeller/attributes.py' %}),
{% endfor %}
}

for name, cls in methods.{{model.name|lower}}.__dict__.items():
    if callable(cls):
        {{model.name}}Dict[name] = cls

{{model.name}} = type(
    str('{{model.name}}'),
    ({{model.unpack}},),
    {{model.name}}Dict
)

{% endfor %}