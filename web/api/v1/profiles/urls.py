from django.urls import path
from . import views



app_name = "profiles"

urlpatterns = [
    path("users_list/", views.UserListView.as_view(), name="user-list"),
    path("me/", views.CurentUserView.as_view(), name="user-list"),
    path("me/<int:pk>/", views.UpdateUserView.as_view(), name="user-update"),
]

"""
        v GET api/v1/profiles/me/
        PUT api/v1/profiles/me/
        POST api/v1/profiles/change/password/
        POST api/v1/profiles/change/avatar/

    """
