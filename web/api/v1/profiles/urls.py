from django.urls import path
from . import views



app_name = "profiles"

urlpatterns = [
    path("users_list/", views.UserListView.as_view(), name="user-list"),
]

"""
        GET api/v1/profiles/me/
        PUT api/v1/profiles/me/
        POST api/v1/profiles/change/password/
        POST api/v1/profiles/change/avatar/

    """
