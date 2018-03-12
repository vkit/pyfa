from __future__ import unicode_literals
import uuid

from django.utils.translation import ugettext_lazy as _

from django.db import models


class TimeStamp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True


class Contact(models.Model):

    contact_name = models.CharField(
        'Contact Name',
        max_length=50, blank=True, null=True)
    company_name = models.CharField(
        'Company Name',
        max_length=50, unique=True)
    pan_no = models.CharField(max_length=50, blank=True, null=True)
    tin_no = models.CharField(max_length=50, blank=True, null=True)
    service_tax_no = models.CharField(max_length=50, blank=True, null=True)
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    credit_days = models.IntegerField(
        verbose_name=_('Credit Period (Days)'), default=0)
    ph_number1 = models.CharField(
        max_length=50,
        blank=True, null=True, verbose_name=_("Phone No."))
    ph_number2 = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("Alternate No."))
    addressline1 = models.CharField(
        max_length=200, verbose_name=_("Addressline 1"), blank=True, null=True)
    addressline2 = models.CharField(
        max_length=200, verbose_name=_("Addressline 2"), blank=True, null=True)
    email = models.EmailField(
        max_length=254, verbose_name=_("E-Mail"), blank=True, null=True)
    zipcode = models.IntegerField(
        verbose_name=_("Zipcode"), blank=True, null=True)
    city = models.CharField(
        max_length=100, verbose_name=_("City"), blank=True, null=True)
    state = models.CharField(
        max_length=100, verbose_name=_("State"), blank=True, null=True)
    country = models.CharField(
        max_length=50, verbose_name=_("Country"), blank=True, null=True)

    class Meta:
        abstract = True
