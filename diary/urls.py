from django.urls import path

from diary import views
from diary.apps import DiaryConfig
from diary.views import (IndexView, NoteCreateView, NoteDeleteView,
                         NoteDetailView, NoteListView, NoteUpdateView,
                         UserNoteListView)

app_name = DiaryConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="home_page"),
    path("note/", NoteListView.as_view(), name="note_list"),
    path("note/create/", NoteCreateView.as_view(), name="note_create"),
    path("note/<int:pk>/detail/", NoteDetailView.as_view(), name="note_detail"),
    path("note/<int:pk>/update/", NoteUpdateView.as_view(), name="note_update"),
    path("note/<int:pk>/delete/", NoteDeleteView.as_view(), name="note_delete"),
    path("search/", views.note_search, name="note_search"),
    path("note/user/<int:pk>", UserNoteListView.as_view(), name="user_note_list"),
]
