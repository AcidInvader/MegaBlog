import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from django.test import Client
from django.contrib.auth import get_user_model
from blog.models import Article
from .fixtures import category, article
pytestmark = [pytest.mark.django_db]

User = get_user_model()


def test_create_article(api_client: Client, user, category, image_content_file):
    url = reverse("api:v1:blog:article-create")
    id = category.id
    data = {
        "title": "test_1.1",
        "image": image_content_file,
        "category": id,
        "content": "Hello this is firs test",
    }
    response = api_client.post(url, data, format="multipart")
    print(response.json())
    assert response.status_code == 201
    print(response.json())
    created_article = Article.objects.last()
    assert created_article.title == "test_1.1"
    assert created_article.author == user
    assert created_article.content == "Hello this is firs test"


def test_list_article(client: Client, article_create):
    url = reverse("api:v1:blog:blog-list")
    article = article_create
    response = client.get(url)
    assert response.status_code == 200
    assert article.title == "Test article"
    assert article.content == "Hello this is for pytest article"
    assert article.image == ""