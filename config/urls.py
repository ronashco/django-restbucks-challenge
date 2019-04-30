from django.conf.urls import url, include
from django.contrib import admin
from core.api import urls as api_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_urls, namespace='api'))
]
