from django import forms
from django.forms import ModelForm
from .models import Space


class supplySpaceForm(ModelForm):
    class Meta:
        model = Space
        fields = ['title', 'capacity', 'address', 'location', 'description']

class CreateNewEvent(forms.Form):
    name = forms.CharField(label="name", max_length=45, required=True)
    description = forms.CharField(label="description", max_length=202, required=False)
    date = forms.DateField(label="date", required=True)
    city = forms.CharField(label="city", max_length=45, required=True)
    place = forms.CharField(label="place", max_length=45, required=True)

