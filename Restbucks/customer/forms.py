from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from customer.models import Order
from django.db import models



class OrderForm(forms.ModelForm):
    production = forms.CharField(max_length=50, required=True)
    consume_location = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Order
        fields = ('production', 'consume_location')