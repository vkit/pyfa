import os

from django.template.loader import get_template

from pyfactory_cnc.settings.base import BASE_DIR

from django.apps import apps


def templatify_auth(base_template, file_name, *args, **kwargs):
    """
    Writes base_templates for authentication
    """
    templates_dir = os.path.normpath(
        os.path.join(BASE_DIR, '../', 'templates'))
    template = get_template(base_template)
    result = template.render(kwargs)
    file = open(
        '{0}/project_base/{1}'.format(
            templates_dir, file_name),
        'w')
    file.write(result)
    file.close()
    return True


def codify_auth(file_name, **kwargs):

    """
    Writes core.url and core.view for authentication
    """
    # Todo: Test
    code_dir = os.path.normpath(
        os.path.join(BASE_DIR, '../', 'core'))
    BaseTemplate = apps.get_model('authentication', 'BaseTemplate')
    kwargs['base_templates'] = BaseTemplate.objects.all()
    template = get_template('authentication/base_core_{0}'.format(file_name))
    result = template.render(kwargs)
    file = open(
        '{0}/{1}'.format(code_dir, file_name),
        'w')
    file.write(result)
    file.close()
    return True
