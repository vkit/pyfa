from django import forms
from django.contrib.auth.models import Group

from .models import BaseTemplate, Tab, SubTab


class BaseTemplateForm(forms.ModelForm):

    class Meta:
        model = BaseTemplate
        fields = "__all__"


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = "__all__"


class TabForm(forms.ModelForm):

    class Meta:
        model = Tab
        fields = "__all__"
        exclude = ('base_template',)


class SubTabForm(forms.ModelForm):

    class Meta:
        model = SubTab
        fields = "__all__"
        exclude = ('tab',)