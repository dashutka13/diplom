from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, ListView, DeleteView, CreateView

from users.forms import UserForm, UserRegisterForm
from users.models import User


class LoginView(BaseLoginView):
    """Контроллер для входа в профиль."""
    template_name = 'users/login.html'
    success_url = reverse_lazy('diary:home_page')


class LogoutView(LoginRequiredMixin, BaseLogoutView):
    """Контроллер для выхода из профиля."""
    pass


class RegisterView(CreateView):
    """Регистрация пользователя."""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование пользователя."""
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:user_list')


class UserListView(LoginRequiredMixin, ListView):
    """Просмотр списка пользователей."""
    model = User


class UserDetailView(LoginRequiredMixin, DetailView):
    """Детали пользователя"""
    model = User
    form_class = UserForm


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление пользователя"""
    model = User
    success_url = reverse_lazy('diary:home_page')

    def test_func(self):
        user = self.request.user
        if not user.is_staff or user.is_superuser:
            return True
        return False
