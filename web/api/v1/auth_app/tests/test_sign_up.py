import pytest
from rest_framework.reverse import reverse
from django.test import Client, override_settings
from django.core import mail
from django.contrib.auth import get_user_model
from .fixtures import sign_up
import re
pytestmark = [pytest.mark.django_db]

User = get_user_model()



mail_settings = override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CELERY_TASK_ALWAYS_EAGER=True,
)

@mail_settings
def test_success_sign_up(client: Client):
    url = reverse("api:v1:auth_app:sign-up")
    data = {
        "first_name": "test1",
        "last_name": "test1",
        "email": "neo@local.com",
        "password_1": "Stasya123",
        "password_2": "Stasya123",
    }
    response = client.post(url, data)
    assert response.status_code == 201
    print(f"{response=}")
    assert len(mail.outbox) == 1
    user = User.objects.get(email=data['email'])
    assert user.first_name == 'test1'
    assert user.last_name == 'test1'
    assert user.check_password('Stasya123')
    assert user.is_active is False
    print(f"{client=}")

class SignUpValidationTest:
    url = reverse("api:v1:auth_app:sign-up")

    def create_data(self, changes: dict) -> dict:
        data = {
            "first_name": "test1",
            "last_name": "test1",
            "email": "neo@local.com",
            "password_1": "Stasya123",
            "password_2": "Stasya123",
        }
        data.update(changes)
        return data
        
    def test_password_not_match(self, client: Client):
        data = self.create_data({"password_2": "Stasya125"})
        response = client.post(self.url, data)
        assert response.status_code == 400
        print(response.json())
        assert response.json() == {'password_2': ['The two password fields did not match']}

    def test_email_wrong(self, client: Client):
        data = self.create_data({"email": "neo"})
        response = client.post(self.url, data)
        assert response.status_code == 400
        print(f"{(response.json())=}")
        print(f"{response=}")
        assert response.json() == {'email': ['Enter a valid email address.']}

    def test_password_length(self, client: Client):
        data = self.create_data({"password_1": "d"})
        response = client.post(self.url, data)
        assert response.status_code == 400
        assert response.json() == {'password_1': ['Ensure this field has at least 8 characters.']}
        print(f"{(response.json())=}")

    def test_password_common(self, client: Client):
        data = self.create_data({"password_1": "qwerty123"})
        response = client.post(self.url, data)
        assert response.status_code == 400
        assert response.json() == {'password_1': ['This password is too common.']}
        print(f"{(response.json())=}")

    def test_password_same_email(self, client: Client):
        data = self.create_data({"password_1": "Neo@localhost.com",
                                 "password_2": "Neo@localhost.com",
                                 "email": "Neo@localhost.com"})
        response = client.post(self.url, data)
        assert response.status_code == 400
        print(f"{(response.json())=}")

@pytest.mark.parametrize(
    ['data', 'response_data'],
    (
        (
            {"password_2": "Stasya125"},
            {'password_2': ['The two password fields did not match']}
        ),
         (
            {"password_1": "d"},
            {'password_1': ['Ensure this field has at least 8 characters.']}
        ),
    )
)
def test_signup_validation(client: Client, data, response_data):
    url = reverse("api:v1:auth_app:sign-up")
    data_ = {
        "first_name": "test1",
        "last_name": "test1",
        "email": "neo@local.com",
        "password_1": "Stasya123",
        "password_2": "Stasya123",
    }
    data_.update(data)
    response = client.post(url, data_)
    assert response.status_code == 400
    assert response.json() == response_data
    print(f'{data_=}')
    print(f'{response_data=}')


@mail_settings
def test_signup_flow(client: Client):
    url_sign_up = reverse("api:v1:auth_app:sign-up")
    url_verify_mail = reverse("api:v1:auth_app:sign-up-verify")
    data = {
        "first_name": "test1",
        "last_name": "test1",
        "email": "neo@local.com",
        "password_1": "Stasya123",
        "password_2": "Stasya123",
    }
    response = client.post(url_sign_up, data)
    assert response.status_code == 201
    user = User.objects.get(email=data['email'])
    assert user.is_active is False
    assert len(mail.outbox) == 1
    letter = mail.outbox[0]
    pattern = r'(http?://[^\"\s]+)'
    result = re.findall(pattern, letter.body)
    print(f"{result=}")
    link = result[0]
    key = link.split('=')[1:]
    data_ = {"key": key[0]}
    print(f"{data_=}")
    response = client.post(url_verify_mail, data_)
    assert response.status_code == 200
    user = User.get_user(key[0])
    assert user.is_active is True


def test_login(client: Client, sign_up):
    url = reverse("api:v1:auth_app:sign-in")
    user = sign_up
    data = {
        "email": user.email,
        "password": "Stasya123",
    }
    response = client.post(url, data)
    assert response.status_code == 200
    print(f"{response.json=}")
    
    




