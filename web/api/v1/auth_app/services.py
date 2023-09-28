from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from typing import TYPE_CHECKING, NamedTuple
from urllib.parse import urlencode, urljoin

import hashlib
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from api.email_services import BaseEmailHandler

from main.decorators import except_shell
from .tasks import send_verify_mail_task
from django.core.mail import send_mail
from django.template import loader

if TYPE_CHECKING:
    from main.models import UserType


User: 'UserType' = get_user_model()


class CreateUserData(NamedTuple):
    first_name: str
    last_name: str
    email: str
    password_1: str
    password_2: str


class ConfirmationEmailHandler(BaseEmailHandler):
    FRONTEND_URL = settings.FRONTEND_URL
    FRONTEND_PATH = '/confirm'
    TEMPLATE_NAME = 'emails/verify_email.html'

    def _get_activate_url(self) -> str:
        url = urljoin(self.FRONTEND_URL, self.FRONTEND_PATH)
        query_params: str = urlencode(
            {
                'key': self.user.confirmation_key,
            },
            safe=':+',
        )
        return f'{url}?{query_params}'

    def email_kwargs(self, **kwargs) -> dict:
        return {
            'subject': _('Register confirmation email'),
            'to_email': self.user.email,
            'context': {
                'user': self.user.full_name,
                'activate_url': self._get_activate_url(),
            },
        }


class AuthAppService:
    @staticmethod
    def is_user_exist(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email: str) -> User:
        return User.objects.get(email=email)

    @transaction.atomic()
    def create_user(self, validated_data: dict):
        data = CreateUserData(**validated_data)
        user = User.objects.create_user(
            first_name=data.first_name, 
            last_name=data.last_name, 
            password=data.password_1,
            email=data.email, 
            is_active=False
        )
        send_verify_mail_task.delay(user.id)
        print(f'Method create_user {data=}')
    

def full_logout(request):
    response = Response({"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK)
    auth_cookie_name = settings.REST_AUTH['JWT_AUTH_COOKIE']
    refresh_cookie_name = settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE']

    response.delete_cookie(auth_cookie_name)
    refresh_token = request.COOKIES.get(refresh_cookie_name)
    if refresh_cookie_name:
        response.delete_cookie(refresh_cookie_name)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except KeyError:
        response.data = {"detail": _("Refresh token was not included in request data.")}
        response.status_code = status.HTTP_401_UNAUTHORIZED
    except (TokenError, AttributeError, TypeError) as error:
        if hasattr(error, 'args'):
            if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                response.data = {"detail": _(error.args[0])}
                response.status_code = status.HTTP_401_UNAUTHORIZED
            else:
                response.data = {"detail": _("An error has occurred.")}
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        else:
            response.data = {"detail": _("An error has occurred.")}
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        message = _(
            "Neither cookies or blacklist are enabled, so the token "
            "has not been deleted server side. Please make sure the token is deleted client side."
        )
        response.data = {"detail": message}
        response.status_code = status.HTTP_200_OK
    return response

class PasswordResetConfirmHandler:
    def __init__(self, password_1: str, password_2: str, uid: str, token: str):
        self.password_1 = password_1
        self.password_2 = password_2
        self.uid = uid
        self.token = token
        
    def validate(self):
        if self.password_1 != self.password_2:
            raise ValidationError("Password's don't match")
        
        pk = urlsafe_base64_decode(self.uid).decode()
        user = User.objects.get(pk=pk)

        if not PasswordResetTokenGenerator().check_token(user, self.token):
            raise ValidationError("The reset token is invalid")
        
        return user
    
    def set_password(self, user):
        user.set_password(self.password_1)
        user.save(update_fields=['password'])

class PasswordResetHandler:
    def __init__(self, email: str):
        self.email = email

    def uid_token_generate(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        return uid, token

    def validate(self) -> User:
        user = User.objects.filter(email=self.email).first()
        if user:
            return user
        else:
            raise ValidationError("User is not exists")


class VerifyEmailHandler:
    def __init__(self, key) -> None:
        self.key = key

    def validate(self):
        user = User.get_user(self.key)
        if user:
            return user
        else:
            raise ValidationError("User is not exists")
        
    def activate_user(self, user):
        user.is_active = True
        user.save(update_fields=['is_active'])
        


class SendEmailHandler:
    def __init__(self, user, uid: str, token: str):
        self.user = user
        self.uid = uid
        self.token = token

    def send_reset_password_mail(self):
        subject = "Reset password mail"
        sender = "hello@localhost"
        recipe = [self.user.email]
        context = {
        'reset_password_url': f"http://127.0.0.1:8888/password-recovery/?uid={self.uid}&token={self.token}",
        'full_name': self.user.first_name,
        }
        html_template = loader.render_to_string('email/reset-password.html', context)
        send_mail(subject, "", sender, recipe, html_message=html_template)


