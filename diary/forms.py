from diary.models import Note
from django import forms

from users.forms import StyleFormMixin


class NoteForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
