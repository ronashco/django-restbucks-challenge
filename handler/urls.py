from django.conf.urls import include, url
from .views import Index

urlpatterns = [
    url(r'^', Index.as_view()),
]
