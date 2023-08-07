from django.urls import path
from . import views



app_name = "profiles"

urlpatterns = [
    path("users_list/", views.UserListView.as_view(), name="user-list"),
]
