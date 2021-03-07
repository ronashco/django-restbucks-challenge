from django.contrib import admin
from django.urls import path

from restbuck_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', views.Menu.as_view()),
    path('test/', views.Features.as_view()),
    path('myorders/', views.MyOrders.as_view()),
    path('myorders/<int:pk>/', views.MyOrder.as_view()),
    ]
