from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms
from django.forms import TextInput

from users.models import User


class StyleFormMixin:
    """Класс для стилизации форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ('is_published', 'usable_password'):
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'gender', 'email', 'password1', 'password2',)


class UserForm(StyleFormMixin, UserChangeForm):
    """Класс-форма для пользователя."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'email', 'password', 'avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Скрывает пароль"""
        self.fields['password'].widget = forms.HiddenInput()
