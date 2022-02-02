from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from django.db import transaction
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from users.models import User
from users.serializers import (UserListSerializer, UserCreateSerializer,)


class ActivateUser(APIView):
    """API view class for user activation"""
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def get(self, request, *args, ** kwargs):
        """Receive email with link and redirect will call this activation request"""
        try:
            uid = urlsafe_base64_decode(kwargs.get("uuid")).decode()
            user = User._default_manager.get(id=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, kwargs.get("token")):
            user.is_active = True
            user.save()
            return Response(data={'text':'Thank you for your email confirmation.'\
                 'Now you can login your account.',}, status=status.HTTP_201_CREATED)
        return Response('Activation link is invalid!', status=status.HTTP_400_BAD_REQUEST)



class UserListAPIView(ListCreateAPIView):
    """API view with base fucntionality for user (list and create)"""
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Creating unactive user function with email sending"""
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)

            ## TODO: Email password is not included in settings.py, SMPT will be not availble

            # safe_url = urlsafe_base64_encode(force_bytes(user.id))
            # current_site = request.get_host()
            # template_context = {
            #     'name': user.first_name,
            #     'settings': settings,
            #     'host': current_site,
            #     'uuid': safe_url,
            #     'token': default_token_generator.make_token(user),
            # }

            # subject = 'Verify your account'
            # template_body = 'email_verification.html'
            # recipient_email = user.email

            # send_email_to_user(subject=subject,
            #                 template_body=template_body,
            #                 recipient_email=recipient_email,
            #                 template_context=template_context)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)