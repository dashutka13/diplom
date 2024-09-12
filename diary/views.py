from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from diary.forms import NoteForm, SearchForm
from diary.models import Note
from users.models import User


class IndexView(TemplateView):
    """Контроллер домашней страницы."""

    template_name = "diary/home_page.html"


class NoteCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания заметки."""

    model = Note
    form_class = NoteForm
    success_url = reverse_lazy("diary:note_list")


class NoteListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка заметок."""

    model = Note
    template_name = "diary/note_list.html"

    def get_queryset(self, *args, **kwargs):
        """
        Получаем отфильтрованный queryset, чтобы пользователь
        мог видеть список только своих заметок, если он не is_staff.
        """
        queryset = super().get_queryset().filter(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class UserNoteListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра заметок конкретного пользователя."""

    model = Note
    template_name = "diary/note_list.html"

    def get_queryset(self):
        """
        Получаем отфильтрованный queryset, чтобы вывести
        список заметок пользователя с конкретным pk.
        """
        queryset = super().get_queryset().filter(owner=self.kwargs.get("pk"))
        return queryset


class NoteDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для детального просмотра заметки."""

    model = Note
    form_class = NoteForm
    template_name = "diary/note_detail.html"


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования заметки."""

    model = Note
    form_class = NoteForm
    success_url = reverse_lazy("diary:note_list")

    def get_success_url(self):
        """Получаем success_url с указанием pk заметки."""
        return reverse("diary:note_detail", args=[self.kwargs.get("pk")])

    def get_object(self, queryset=None):
        """Исключает возможность редактирования пользователем чужой заметки."""
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не можете редактировать чужие заметки!")
        return self.object


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаление заметки."""

    model = Note
    success_url = reverse_lazy("diary:note_list")

    def get_object(self, queryset=None):
        """Исключает возможность удаления пользователем чужой заметки."""
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не можете удалять чужие заметки!")
        return self.object


def note_search(request):
    """
    Функция для реализации поиска заметок по запросу пользователя.
    Поиск осуществляется в полях 'topic' и 'body'.
    """
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = Note.objects.annotate(
                search=SearchVector(
                    "topic",
                    "body",
                ),
            ).filter(search=query)
    return render(
        request, "diary/search.html", {"form": form, "query": query, "results": results}
    )
