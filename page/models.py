from __future__ import unicode_literals

from django.db import models

from base.models import TimeStamp

from django.core.urlresolvers import reverse


PageTypes = (
    ('GenericDataGridView', 'Generic Data Grid'),
    ('GenericJobCard', 'JobCard'),
    ('GenericInvoice', 'Invoice'),
)


class Page(TimeStamp):

    app = models.ForeignKey('app.App')
    model = models.ForeignKey('modeller.ModelObject', null=True)
    page_type = models.CharField(max_length=50, choices=PageTypes)
    base_templates = models.ManyToManyField(
        'authentication.BaseTemplate', related_name='base_templates')
    name = models.CharField(max_length=50, blank=True)
    list_display = models.ManyToManyField('modeller.ModelField')
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=50, blank=True, default='')
    date_range = models.BooleanField(default=False)
    check_box = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def url_pattern(self):
        return 'list/'

    def url_reverse(self):
        return '{0}:{1}'.format(self.model.app.code_name(), self.url_name())

    def url_name(self):
        return 'list'

    def url_full_path(self):
        return reverse(self.url_reverse())
