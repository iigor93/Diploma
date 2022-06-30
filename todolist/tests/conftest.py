import pytest
import factory
from datetime import datetime
from pytest_factoryboy import register

from django.utils import timezone
from goals.models import Board, GoalCategory, Goal, GoalComment


pytest_plugins = "tests.fixtures"


@register
class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board
    
    title = 'test_board_title'
        
        
@register
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory
        
    title = 'test_category_title'


@register
class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal
    
    due_date = datetime.now(tz=timezone.utc)
    description = 'some description'

@register
class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment
