import pytest
from rest_framework.reverse import reverse
from django.test import Client, override_settings
from django.core import mail
from django.contrib.auth import get_user_model
pytestmark = [pytest.mark.django_db]

User = get_user_model()

@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    # CELERY_TASK_ALWAYS_EAGER=True,
)
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


class MailIntegrationTest:
    pass
        

