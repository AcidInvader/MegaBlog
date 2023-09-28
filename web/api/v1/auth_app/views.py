from dj_rest_auth import views as auth_views
from django.contrib.auth import logout as django_logout
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core import signing
from main.models import User
from rest_framework.exceptions import Throttled
from .services import PasswordResetConfirmHandler, PasswordResetHandler, SendEmailHandler, VerifyEmailHandler


from . import serializers
from .services import AuthAppService, full_logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import send_reset_password_mail
from .tasks import send_reset_password_mail_task


class SignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = AuthAppService()
        service.create_user(serializer.validated_data)
        return Response(
            {'detail': _('Confirmation email has been sent')},
            status=status.HTTP_201_CREATED,
        )


class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        response = full_logout(request)
        return response


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        print('Data from serializer', serializer)
        serializer.is_valid(raise_exception=True)
        service = PasswordResetHandler(**serializer.data)
        user = service.validate()
        uid, token = service.uid_token_generate(user)
        send_reset_password_mail_task.delay(user, uid, token)

        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK,
        )
        

class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = PasswordResetConfirmHandler(**serializer.data)
        user = service.validate()
        service.set_password(user)
        
        return Response(
            {'detail': _('Password has been reset with the new password.')},
            status=status.HTTP_200_OK,
        )
      


class VerifyEmailView(GenericAPIView):
    serializer_class = serializers.VerifyEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = VerifyEmailHandler(**serializer.data)
        user = service.validate()
        service.activate_user(user)
        
        return Response(
            {'detail': _('Email verified')},
            status=status.HTTP_200_OK,
        )
