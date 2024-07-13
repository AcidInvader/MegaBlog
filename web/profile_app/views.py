from django.shortcuts import render
from main.views import TemplateAPIView
from rest_framework.permissions import IsAuthenticated 


class ProfileView(TemplateAPIView):
    permission_classes = (IsAuthenticated,)
