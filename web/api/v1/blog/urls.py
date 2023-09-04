from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('blog/', views.BlogListView.as_view(), name="blog-list"),
    path('blog/category-list', views.CategoryListView.as_view(), name="category-list"),
    path('blog/create-article/', views.ArticleCreateView.as_view(), name="article-create"),
    path('blog/create-comment/', views.CommentCreateView.as_view(), name="create-comment"),
    path('blog/comment-list/<int:article_pk>/', views.CommentListView.as_view(), name="comment-list"),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name="article-detail"),
    path('blog/<str:slug>', views.SlugDetailView.as_view(), name="article-detail"),
]

