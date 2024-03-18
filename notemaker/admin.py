from django.contrib import admin
from .models import NoteMakerModel

@admin.register(NoteMakerModel)
class NoteMakerAdmin(admin.ModelAdmin):
    list_display = ['youtubeLink', 'processing', 'noteType']
