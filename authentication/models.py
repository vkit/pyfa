from __future__ import unicode_literals
import os

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import Group

from base.models import TimeStamp

from .utils import templatify_auth, codify_auth

from pyfactory_cnc.settings.base import BASE_DIR


class BaseTemplate(TimeStamp):

    name = models.CharField(max_length=50,
        help_text="Note: Authentication Level Name should be one word. \n (Example: 'Marketing', 'Production', 'Vendors' etc)  "
        "Authentication level is set for funcationality or pages a perticular group/department or set of groups/department can access")
    groups = models.ManyToManyField(Group,
        help_text="Select one or more groups that can access this Authentication level")

    def __unicode__(self):
        return self.name

    def file_name(self):
        """
        Returns the string for using as template file name
        """
        return "{0}_base_dashboard.html".format(self.name.lower())

    def dashboard_view_name(self):
        """
        Returns the string for using as Dashboard View name in core app
        """
        return "{0}DashboardView".format(self.name.capitalize())

    def dashboard_url(self):
        """
        Returns the string for using as url to Dashboard View in core app
        """
        return "{0}_dashboard/".format(self.name.lower())

    def build_auth(self):
        """
        Creates/Updates authentication system
        This methods creates/updates
        project_base/<somebasetemplate>.html file
        """
        tabs = self.tab_set.all()
        templatify_auth(
            base_template='base/master_base.html',
            file_name=self.file_name(),
            tabs=tabs,
        )

    def templatified(self):
        template_dir = os.path.normpath(
            os.path.join(BASE_DIR, '../', 'templates'))
        is_file = os.path.isfile(
            '{0}/project_base/{1}'.format(template_dir, self.file_name()))
        if is_file:
            return True
        else:
            return False


@receiver(post_save, sender=BaseTemplate, dispatch_uid="update_stock_count")
def update_auth(sender, instance, **kwargs):
    """
    Creates urls and view files in core app after saving each basetemplates"""
    codify_auth(file_name='views.py')
    codify_auth(file_name='urls.py')


class Tab(TimeStamp):

    name = models.CharField(max_length=50)
    base_template = models.ForeignKey(BaseTemplate)
    url = models.CharField(max_length=200, blank=True)
    page = models.ForeignKey(
        'page.Page', related_name='tabs', null=True, blank=True)

    def __unicode__(self):
        return "{0}-{1}".format(self.base_template, self.name)


class SubTab(TimeStamp):

    name = models.CharField(max_length=50)
    tab = models.ForeignKey(Tab)
    url = models.CharField(max_length=200, blank=True)
    page = models.ForeignKey(
        'page.Page', related_name='subtabs', null=True, blank=True)

    def __unicode__(self):
        return "{0}-{1}".format(self.tab, self.name)
