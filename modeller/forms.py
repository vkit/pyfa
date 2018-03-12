from django import forms

from .models import ModelObject, ModelField, INHERITOBJ


class ModelObjectForm(forms.ModelForm):
    inherit = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=INHERITOBJ)

    class Meta:
        model = ModelObject
        fields = "__all__"


class ModelFieldForm(forms.ModelForm):
    # Fetching model objects for FK
    # options = [(model_obj.code_name(), model_obj.code_name()) for model_obj in ModelObject.objects.all()]
    # options.insert(0, ('', 'Select'))
    # print options
    options = ('', '')
    foreign_key = forms.ChoiceField(choices=options, required=False)
    many_to_many_key = forms.ChoiceField(choices=options, required=False)

    class Meta:
        model = ModelField
        exclude = ('model_obj',)
