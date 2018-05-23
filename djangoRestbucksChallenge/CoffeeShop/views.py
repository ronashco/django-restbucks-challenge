from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from djangoRestbucksChallenge.CoffeeShop import forms


def home(request):
    return render(request, 'base.html')


def signin(request):
    form = forms.LoginForm()
    if request.method == 'GET':
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        customer = authenticate(request, username=username, password=password)
        if customer is not None:
            login(request, customer)
            return HttpResponseRedirect(reverse('panel'))
        else:
            return render(request, 'login.html', {'form': form, 'error_message': "error in authentication!"})
