from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView

from users.forms import UserRegisterForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('diary:home_page')


class LogoutView(LoginRequiredMixin, BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    # def form_valid(self, form):
    #     self.object = form.save()
    #     send_mail(
    #         subject='Поздравляем с регистрацией!',
    #         message='Вы зарегистрировались на нашей платформе, добро пожаловать!',
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[self.object.email]
    #     )
    #     return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование пользователя"""
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:user_list')


class UserListView(LoginRequiredMixin, ListView):
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
