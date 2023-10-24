import pytest
from django.test import Client, override_settings
from django.core import mail
from django.contrib.auth import get_user_model
import re
from django.core.files.base import ContentFile
from base64 import b64decode
from rest_framework_simplejwt.tokens import RefreshToken

from typing import NamedTuple

pytestmark = [pytest.mark.django_db]

User = get_user_model()

@pytest.fixture
def user() -> User:
    user = User.objects.create_user(
        first_name = "test1", 
        last_name = "test1", 
        password = "Stasya123",
        email = "neo@local.com", 
        is_active=True
        )

    return user


raw_image: str = (
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAA'
    'AA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjYAAAAAIAAeIhvDMAAAAASUVORK5CYII='
)


@pytest.fixture()
def image_content_file() -> ContentFile:
    _format, _raw_image = raw_image.split(';base64,')
    ext = _format.split('/')[-1]
    return ContentFile(b64decode(_raw_image), name=f'image.{ext}')


class UserToken(NamedTuple):
    access_token: str
    refresh_token: str


@pytest.fixture()
def user_tokens(user) -> UserToken:
    refresh: RefreshToken = RefreshToken().for_user(user)
    return UserToken(access_token=refresh.access_token, refresh_token=str(refresh))


@pytest.fixture()
def api_client(client: Client, user_tokens) -> Client:
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {user_tokens.access_token}'
    # client.cookies
    return client
