from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^panel', views.panel, name='panel'),
    url(r'^menu', views.menu, name='menu'),
    url(r'^logout', views.signout, name='logout'),
]
