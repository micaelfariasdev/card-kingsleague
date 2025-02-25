from django.contrib import admin
from .models import CardCreate


@admin.register(CardCreate)
class CardCreateAdmin(admin.ModelAdmin):
    ...
