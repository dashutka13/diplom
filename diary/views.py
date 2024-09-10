from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from diary.models import Note
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from diary.forms import NoteForm


class IndexView(TemplateView):
    """Контроллер домашней страницы."""
    template_name = 'diary/home_page.html'


class NoteCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания заметки."""
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy('diary:home_page')


class NoteListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка заметок."""
    model = Note
    template_name = 'diary/note_list.html'


class NoteDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для детального просмотра заметки."""
    model = Note
    form_class = NoteForm
    template_name = 'diary/note_detail.html'


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования заметки."""
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy('diary:note_list')


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаление заметки."""
    model = Note
    success_url = reverse_lazy('diary:home_page')

    def test_func(self):
        user = self.request.user
        if not user.is_staff or user.is_superuser:
            return True
        return False


class UserNoteListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка заметок пользователя."""
    model = Note
    template_name = 'diary/note_list.html'
