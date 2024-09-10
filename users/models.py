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

    email = models.EmailField(unique=True, verbose_name='Email', help_text='Укажите email')

    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', help_text='Загрузите аватар', **NULLABLE)

    """Указание гендера необходимо для выбора подходящей заглушки аватара."""
    gender = models.CharField(choices=GENDERS, verbose_name='пол', help_text='Выберите пол', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
