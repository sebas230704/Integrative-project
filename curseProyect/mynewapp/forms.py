from django import forms


class CreateNewName(forms.Form):
    name = forms.CharField(label="nombre", max_length=200, required=True)
    lastName = forms.CharField(label="apellido", max_length=200, required=True)
