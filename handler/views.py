from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class Index(TemplateView):
    def get(self, *args, **kwargs):
        return render(self.request, 'handler/index.html')


class Login(TemplateView):
    def post(self, *args, **kwargs):
        decoded_request = QueryDict(self.request.body)
        """
        we consider username is email
        """
        username = decoded_request['email']
        password = decoded_request['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('/home/')
        else:
            return render(self.request, 'handler/incorrect.html')


decorators = [login_required]


@method_decorator(decorators, name='dispatch')
class Home(TemplateView):
    def get(self, *args, **kwargs):
        print("wwefjksdfn")
        return render(self.request, 'handler/home.html')


class Logout(TemplateView):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('/')
