from django.db import models

from core.models import User


class TgUser(models.Model):
    """Класс пользователя Телеграмм, связь с пользователем django"""
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)
    
    chat_tgid = models.CharField(max_length=20, verbose_name="Чат id",)
    user_tgid = models.CharField(max_length=20, unique=True, verbose_name="Пользователь id",)
    
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tg_category", null=True)
