from django.conf.urls import include, url
from views import MenuListAPIVeiw


urlpatterns = [
    url(r'^$', MenuListAPIVeiw.as_view(), name="menu"),
    url(r'^menu/', MenuListAPIVeiw.as_view(), name="menu"),
]
