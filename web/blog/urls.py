from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from main.views import TemplateAPIView, PostCreateView

app_name = 'blog'

router = DefaultRouter()
router.register('posts', views.ArticleViewSet, basename='post')

urlpatterns = [
    path('blog/', TemplateAPIView.as_view(template_name='blog/post_list.html'), name='blog-list'),
    path('blog/article/create', PostCreateView.as_view(template_name='blog/post_create.html'), name='post-create'),
    path('blog/article', TemplateAPIView.as_view(template_name='blog/post_detail.html'), name='post-detail'),
]

urlpatterns += router.urls
