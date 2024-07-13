from django.urls import path
from django.views.generic import TemplateView
from .views import ProfileView

from main.views import TemplateAPIView

app_name = 'profile_app'


urlpatterns = [
    path("profile/", ProfileView.as_view(template_name="profile/profile.html"), name="profile_page"),
]