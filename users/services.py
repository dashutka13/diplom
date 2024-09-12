from django.core.mail import send_mail
from django.conf import settings


def send_new_password(email, new_password):
    """Функция для отправки пользователю нового пароля."""
    send_mail(
        subject='Вы сменили пароль!',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
