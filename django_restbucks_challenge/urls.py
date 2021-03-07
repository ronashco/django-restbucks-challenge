from django.contrib import admin
from django.urls import path

from restbuck_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', views.Menu.as_view()),
    ]
