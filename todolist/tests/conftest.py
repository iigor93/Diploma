from datetime import datetime

from django.utils import timezone

import factory

from goals.models import Board, Goal, GoalCategory, GoalComment

from pytest_factoryboy import register


pytest_plugins = "tests.fixtures"


@register
class BoardFactory(factory.django.DjangoModelFactory):
    """board class"""
    class Meta:
        model = Board
    
    title = 'test_board_title'
        
        
@register
class CategoryFactory(factory.django.DjangoModelFactory):
    """category class"""
    class Meta:
        model = GoalCategory
        
    title = 'test_category_title'


@register
class GoalFactory(factory.django.DjangoModelFactory):
    """goal class"""
    class Meta:
        model = Goal
    
    due_date = datetime.now(tz=timezone.utc)
    description = 'some description'


@register
class CommentFactory(factory.django.DjangoModelFactory):
    """comment factory"""
    class Meta:
        model = GoalComment
