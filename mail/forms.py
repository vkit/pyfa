from django import forms


class EmailForm(forms.Form):
    # from_email = forms.CharField()
    to_email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
