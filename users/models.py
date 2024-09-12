from django.contrib.auth.models import AbstractUser
from django.db import models
from diary.models import NULLABLE


class User(AbstractUser):
    FEMALE_GENDER = 'female'
    MALE_GENDER = 'male'

    GENDERS = (
        (FEMALE_GENDER, 'женский'),
        (MALE_GENDER, 'мужской')
    )

    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', help_text='Загрузите аватар', **NULLABLE)

    """Указание гендера необходимо для выбора подходящей заглушки аватара."""
    gender = models.CharField(choices=GENDERS, verbose_name='пол', help_text='Выберите пол', **NULLABLE)

    verify_key = models.CharField(**NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='статус аккаунта')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
