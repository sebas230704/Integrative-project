from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class supplySpaceForm(ModelForm):
    class Meta:
        model = Space
        fields = ['title', 'capacity', 'address', 'location', 'description']

class CreateNewEvent(forms.Form):
    name = forms.CharField(label="name", max_length=45, required=True)
    description = forms.CharField(label="description", max_length=808, required=False)
    date = forms.DateField(label="date", required=True)
    city = forms.CharField(label="city", max_length=45, required=True)
    place = forms.CharField(label="place", max_length=45, required=True)
    categories = forms.ModelMultipleChoiceField(
        queryset=EventCategories.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    image = forms.ImageField(required=True)

    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'city', 'place', 'categories', 'image']


class CreateOrganizer(forms.Form):
    companyName = forms.CharField(label="Company Name", max_length=99, required=True)
    description = forms.CharField(label="Description", max_length=808, required=True)
    telefono = forms.CharField(label="Telefono", max_length=20)
    email = forms.CharField(label="Email", max_length=99, required=True)
    specialties = forms.ModelMultipleChoiceField(
        queryset= Specialties.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['description', 'likes', 'location']
        
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()