from django import forms
from django.forms import ModelForm
from CoffeeShop import models

from django.contrib.auth import authenticate


class LoginForm(ModelForm):

    class Meta:
        model = models.Customer
        fields = ['username', 'password']
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'})
        }

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data["username"]
        password = cleaned_data["password"]
        user = authenticate(self.data, username=username, password=password)

        if user is None:
            raise forms.ValidationError("Error")

        return cleaned_data