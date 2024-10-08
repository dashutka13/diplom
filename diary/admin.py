from django.contrib import admin

from diary.models import Note


@admin.register(Note)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "topic",
        "body",
        "owner",
    )
    list_filter = ("owner",)
    search_fields = (
        "topic",
        "body",
    )
