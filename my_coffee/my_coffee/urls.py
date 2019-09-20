from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    # Examples:
    # url(r'^$', 'my_coffee.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/productions/', include("productions.api.urls",
                                      namespace="productions-api")),
    url(r'^api/customers/', include("customers.api.urls",
                                    namespace="customers-api")),
    url(r'^api/token/auth/', obtain_jwt_token),
]
