import pytest
from rest_framework.test import APIClient
from blog.models import Category, Article
from api.v1.auth_app.tests.fixtures import sign_up


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def category():
    cat = Category.objects.create(name = "it")
    return cat


@pytest.fixture
def article_create(sign_up, category):
    user = sign_up
    category = category
    article = Article.objects.create(category=category,
                                     title="Test article",
                                     content="Hello this is for pytest article",
                                     image="",
                                     author=user,
                                     )
    
    return article
