from django.urls import path
from django.views.generic import TemplateView

from main.views import TemplateAPIView

app_name = 'profile_app'


urlpatterns = [
    path("profile/", TemplateAPIView.as_view(template_name="profile/profile.html"), name="profile_page"),
]