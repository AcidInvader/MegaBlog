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

    def test_password_not_match(self, client: Client):
        url = reverse("api:v1:auth_app:sign-up")
        data = {
            "first_name": "test1",
            "last_name": "test1",
            "email": "neo@local.com",
            "password_1": "Stasya123",
            "password_2": "Stasya124",
        }
        response = client.post(url, data)
        assert response.status_code == 400
        print(response.json())
        assert response.json() == {'password_2': ['The two password fields did not match']}

