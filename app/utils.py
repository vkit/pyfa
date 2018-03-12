# from djangomom.settings.base import BASE_DIR
import os
from django.core.management import call_command

from django.template.loader import get_template

from pyfactory_cnc.settings.base import PROJECT_APPS_DIR

import logging
logger = logging.getLogger(__name__)


def startapp(app_code_name):
    """
    Generates source codes, this method is
    equivalent to django startapp command.
    Needs app_code_name arg as foldername
    """
    logger.debug('App name {0}'.format(app_code_name))
    folder = os.system('mkdir {0}/{1}'.format(
        PROJECT_APPS_DIR,
        app_code_name
    )
    )
    if folder == 0:
        return call_command("startapp", app_code_name, '{0}/{1}'.format(
            PROJECT_APPS_DIR,
            app_code_name),
            "--template=sampleapp"
        )
    else:
        return False


def makemigrations(app_name):
    """
    """
    call_command('makemigrations', app_name, interactive=False)


def migrate(app_name):
    """
    """
    call_command('migrate', app_name, interactive=False)


def codify(app_name, template, file, *args, **kwargs):
    """
    Writes python files with given app, file and template
    """
    template = get_template(template)
    result = template.render(kwargs)
    file = open(
        '{2}/{0}/{1}.py'.format(
            app_name,
            file,
            PROJECT_APPS_DIR),
        'w')
    file.write(result)
    file.close()
