from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^products/$', views.Menu.as_view(), name='menu'),
    url(r'^accounts/register/$', views.register, name='register')
]
