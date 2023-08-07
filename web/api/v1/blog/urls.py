from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('blog/', views.BlogListView.as_view(), name="blog-list"),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name="article-detail"),
    path('blog/<str:slug>', views.SlugDetailView.as_view(), name="article-detail"),
]

