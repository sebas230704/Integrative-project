from django.forms import ModelForm
from .models import Space

class supplySpaceForm(ModelForm):
    class Meta:
        model = Space
        fields = ['title', 'capacity', 'address', 'location', 'description']