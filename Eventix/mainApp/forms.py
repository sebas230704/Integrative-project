from django import forms
from django.forms import ModelForm
from .models import *


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
    categories = forms.ModelMultipleChoiceField(
        queryset=EventCategories.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class CreateOrganizer(forms.Form):
    companyName = forms.CharField(label="Company Name", max_length=99, required=True)
    description = forms.CharField(label="Description", max_length=202, required=True)
    specialties = forms.ModelMultipleChoiceField(
        queryset= Specialties.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
