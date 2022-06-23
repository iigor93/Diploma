from django.db import models
from django.utils import timezone

from core.models import User

class DatesModelMixin(models.Model):
    class Meta:
        abstract = True 

    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)


class Status(models.IntegerChoices):
    TO_DO = 1, "К выполнению"
    IN_PROGRESS = 2, "В процессе"
    DONE = 3, "Выполнено"
    ARCHIVED = 4, "Архив"

class Priority(models.IntegerChoices):
    LOW = 1, "Низкий"
    MEDIUM = 2, "Средний"
    HIGH = 3, "Высокий"
    CRITICAL = 4, "Критический"

   

class Board(DatesModelMixin):
    class Meta:
        verbose_name = "Доска" 
        verbose_name_plural = "Доски"
    
    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удаленo", default=False)
    
    

class GoalCategory(DatesModelMixin):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories")

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    

class Goal(DatesModelMixin):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.CharField(verbose_name='Описание', max_length=2000)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT)
    due_date = models.DateTimeField(verbose_name='Дата выполнения')
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    status = models.PositiveSmallIntegerField(verbose_name="Статус", 
        choices=Status.choices, default=Status.TO_DO)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", 
        choices=Priority.choices, default=Priority.MEDIUM)


class GoalComment(DatesModelMixin):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    text = models.CharField(verbose_name="Комментарий", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE)
 

class BoardParticipant(DatesModelMixin):
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        OWNER = 1, "Владелец"
        WRITER = 2, "Редактор"
        READER = 3, "Читатель"

    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="participants",)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT, related_name="participants",)
    role = models.PositiveSmallIntegerField(verbose_name="Роль", choices=Role.choices, default=Role.OWNER)
    

    
