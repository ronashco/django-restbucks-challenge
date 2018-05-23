from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def signout(request):
    current_user = request.user
    if current_user is not None:
        logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def panel(request):
    return render(request, 'panel.html')