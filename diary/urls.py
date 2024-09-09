from django.urls import path

from diary.apps import DiaryConfig
from diary.views import IndexView, NoteCreateView

app_name = DiaryConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='home_page'),
    path("note/create/", NoteCreateView.as_view(), name="note-create"),
]
