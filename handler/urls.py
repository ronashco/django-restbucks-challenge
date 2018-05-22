from django.conf.urls import include, url
from .views import Index, Login, Home, Logout, AddOrder, DeleteOrder

urlpatterns = [
    url(r'^$', Index.as_view()),
    url(r'^login$', Login.as_view()),
    url(r'^home/logout', Logout.as_view()),
    url(r'^home/logout/', Logout.as_view()),
    url(r'^home$', Home.as_view()),
    url(r'^home/$', Home.as_view()),
    url(r'^home/addorder', AddOrder.as_view()),
    url(r'^home/addorder/', AddOrder.as_view()),
    url(r'^home/deleteorder/(?P<order_id>\d+)/$', DeleteOrder.as_view()),
    url(r'^home/deleteorder/(?P<order_id>\d+)$', DeleteOrder.as_view()),
]
