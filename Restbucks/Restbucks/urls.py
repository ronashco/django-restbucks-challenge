from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', include('customer.urls'), name='customer'),
    path('admin/', admin.site.urls),
]