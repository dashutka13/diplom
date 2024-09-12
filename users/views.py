import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import UpdateView, DetailView, ListView, DeleteView, CreateView

from config import settings
from users.forms import UserForm, UserRegisterForm
from users.models import User
from users.services import send_new_password


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

    def form_valid(self, form):
        new_user = form.save()

        token = get_random_string(length=50)
        new_user.verify_key = token

        new_user.save()

        current_site = get_current_site(self.request)

        send_mail(
            subject='Завершение регистрации',
            message=f'Для подтверждения электронной почты перейдите по следующей ссылке: \n'
                    f'http://{current_site.domain}{reverse("users:verify", kwargs={"uid": new_user.pk, "token": token})}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],

        )
        return super().form_valid(form)


class VerifyView(View):
    def get(self, request, uid, token):
        user = get_object_or_404(User, pk=uid, verify_key=token)
        user.is_verified = True
        user.save()
        return render(request, 'users/verified.html')


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_verified:
            return render(request, "users/verify_info.html")
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования пользователя."""
    model = User
    form_class = UserForm

    def get_success_url(self):
        """Получаем success_url с указанием pk пользователя."""
        return reverse('users:user_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        """Исключает возможность редактирования объекта пользователя другим пользователем,
        не являющимся администратором."""
        self.object = super().get_object(queryset)
        if self.object != self.request.user and not self.request.user.is_staff:
            raise Http404('Вы не можете редактировать профили других пользователей!')
        return self.object


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
    success_url = reverse_lazy('users:user_list')

    def get_object(self, queryset=None):
        """Исключает возможность удаления объекта пользователя другим пользователем,
        не являющимся администратором."""
        self.object = super().get_object(queryset)
        if self.object != self.request.user and not self.request.user.is_staff:
            raise Http404('Вы не можете удалять других пользователей!')
        return self.object


@login_required
def generate_new_password(request):
    """Контроллер для генерации нового пароля"""
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])

    request.user.set_password(new_password)
    request.user.save()

    send_new_password(request.user.email, new_password)
    return render(request, 'users/password_generated.html')
