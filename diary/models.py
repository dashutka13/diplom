from django.db import models
from config import settings

NULLABLE = {'blank': True, 'null': True}


class Note(models.Model):
    """Модель заметки"""
    topic = models.CharField(max_length=50, verbose_name="заголовок")
    body = models.TextField(verbose_name="содержание заметки")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="владелец")

    def __str__(self):
        return f"{self.topic}: {self.body}"

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
