from django.contrib import admin
from actions.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "content_type", "vote", "created_at", "content_object")

