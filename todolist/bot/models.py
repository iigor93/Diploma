from django.db import models

from core.models import User
from goals.models import GoalCategory


class TgUser(models.Model):
    
    class Conditions(models.IntegerChoices):
        BEGIN = 1, "Начальное состояние"
        CHOOSE_CATEGORY = 2, "Ожидание названия для категории"
        GOAL_CREATE = 3, "Ожидание названия для цели"

    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)
    
    chat_tgid = models.CharField(max_length=20, verbose_name="Чат id",)
    user_tgid = models.CharField(max_length=20, unique=True, verbose_name="Пользователь id",)
    
    verification_code = models.CharField(max_length=10, verbose_name='Проверочный код')
    
    condition = models.PositiveSmallIntegerField(verbose_name="состояние",
                                                 choices=Conditions.choices, default=Conditions.BEGIN)
    
    category = models.ForeignKey(GoalCategory, on_delete=models.PROTECT, related_name="tg_user", null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tg_category", null=True)
