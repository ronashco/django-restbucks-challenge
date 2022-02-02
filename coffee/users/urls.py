from django.urls import path
from users.views import (UserListAPIView, ActivateUser)

urlpatterns = [
    path('', UserListAPIView.as_view(), name="users_list"),
    path('activate/<uuid>/<token>/', ActivateUser.as_view(), name='activate_account'),
]

