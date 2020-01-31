from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^menu$', views.ProductListAPIView.as_view(), name='menu'),
    url(r'^create$', views.ProductCreateAPIView.as_view(), name='create'),

]