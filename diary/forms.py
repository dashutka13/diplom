from django.forms import TextInput

from diary.models import Note
from django import forms

from users.forms import StyleFormMixin


class NoteForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
        widgets = {
            """Указываем placeholder для полей ввода заголовка и содержания заметки."""
            'topic': TextInput(attrs={'placeholder': 'Укажите заголовок заметки...'}),
            'body': TextInput(attrs={'placeholder': 'Введите текст заметки...'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField()
