from django.views.generic import CreateView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin

from diary.models import Note
from diary.serializers import NoteSerializer
from users.permissions import IsModer
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from diary.forms import NoteForm

class IndexView(TemplateView):
    template_name = 'diary/home_page.html'


class NoteCreateView(LoginRequiredMixin, CreateView):
    """Создание заметки"""
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy('diary:home_page')
