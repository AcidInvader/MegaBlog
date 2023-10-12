import pytest
from django.test import Client, override_settings
from django.core import mail
from django.contrib.auth import get_user_model
import re
pytestmark = [pytest.mark.django_db]

User = get_user_model()

@pytest.fixture
def sign_up() -> User:
    user = User.objects.create_user(
        first_name = "test1", 
        last_name = "test1", 
        password = "Stasya123",
        email = "neo@local.com", 
        is_active=True
        )
    

    return user


@pytest.fixture
def login_user(client: Client, sign_up) -> User:
    user = sign_up
    client.login(email=user.email, password="Stasya123")

    return user


