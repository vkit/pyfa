from __future__ import unicode_literals

from django.db import models

from base.models import TimeStamp


INHERITOBJ = (
    (0, 'Contact'),
    (1, 'TimeStamp'),
)


class ModelObject(TimeStamp):

    app = models.ForeignKey('app.App')
    name = models.SlugField(max_length=50, blank=True, unique=True)
    inherit = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name.capitalize()

    def fields_count(self):
        return self.modelfield_set.count()

    def code_name(self):
        return '{1}.{0}'.format(self.name.capitalize(), self.app.code_name())

    def unpack(self):
        import ast
        inheritance_list = [INHERITOBJ[int(obj)][1] for obj in ast.literal_eval(self.inherit)]
        return ','.join(inheritance_list)

FieldTypes = (
    (1, 'AutoField'),
    (2, 'IntegerField'),
    (3, 'FloatField'),
    (4, 'DateField'),
    (5, 'DateTimeField'),
    (6, 'EmailField'),
    (7, 'TimeField'),
    (8, 'DecimalField'),
    (9, 'CharField'),
    (10, 'SlugField'),
    (11, 'TextField'),
    (12, 'URLField'),
    (13, 'BigIntegerField'),
    (14, 'SmallIntegerField'),
    (15, 'PositiveSmallIntegerField'),
    (16, 'BooleanField'),
    (17, 'ForeignKey'),
    (18, 'ManyToManyField'),
    (19, 'OneToOneField'),
    (20, 'DurationField')
)


class ModelField(TimeStamp):

    model_obj = models.ForeignKey(ModelObject)
    name = models.SlugField(max_length=50, blank=True)
    field_type = models.IntegerField(
        blank=True, choices=FieldTypes)
    max_length = models.IntegerField(blank=True, null=True)
    default = models.CharField(max_length=50, blank=True, null=True)
    blank = models.BooleanField(default=False)
    null = models.BooleanField(default=False)
    unique = models.BooleanField(default=False)
    foreign_key = models.CharField(max_length=100, blank=True, null=True)
    many_to_many_key = models.CharField(max_length=50, blank=True, null=True)
    related_name = models.CharField(max_length=50, blank=True, null=True)
    max_digits = models.IntegerField(blank=True, null=True)
    decimal_places = models.IntegerField(blank=True, null=True)
    choices = models.CharField(
        max_length=500, blank=True,
        help_text="Add a Python Tupple ((1, 'Today'),(2, 'Tomorrow'),")

    def __unicode__(self):
        return "{0}-{1}".format(self.model_obj, self.name)

    class Meta:
        unique_together = (
            ('name', 'model_obj'),
        )
