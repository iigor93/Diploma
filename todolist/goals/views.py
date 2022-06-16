from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant, Status
from goals.serializers import GoalCategoryCreateSerializer, GoalCategoryListSerializer, GoalCreateSerializer, GoalListSerializer
from goals.serializers import GoalCommentCreateSerializer, GoalCommentListSerializer
from goals.serializers import BoardCreateSerializer, BoardListSerializer, BoardSerializer
from goals.filters import GoalDateFilter

from goals.permissions import BoardPermissions, GoalCategoryCreatePermissions, GoalPermissions, GoalDetailPermissions, GoalCommentCreatePermissions





class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated, GoalCategoryCreatePermissions]
    serializer_class = GoalCategoryCreateSerializer
    

class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    prmission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryListSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["title"]
    filterset_fields = ['board']
    
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    
    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)
        

class GoalCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        current_user = request.user
        
        board_participant = BoardParticipant.objects.filter(user=current_user, board=instance.board).first()
        
        if board_participant.role == BoardParticipant.Role.OWNER or board_participant.role == BoardParticipant.Role.WRITER:
            return super().update(request, *args, **kwargs)
        else:
            raise ValidationError({'Permissions': 'No permissions for this action'})
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        goals = instance.goal_set.all()
        for goal in goals:
            goal.is_deleted = True
            goal.save()
        return instance


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated, GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    prmission_classes = [permissions.IsAuthenticated, GoalPermissions]
    serializer_class = GoalListSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["title", 'description']
    filterset_class = GoalDateFilter
    
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    
    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user, is_deleted=False)


class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalListSerializer
    permission_classes = [permissions.IsAuthenticated, GoalDetailPermissions]
    
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["title", 'description']
    
    ordering_fields = ["title", "created"]
    ordering = ["title"]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user, is_deleted=False)
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated, GoalCommentCreatePermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    prmission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentListSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    
    filterset_fields = ['goal']
    search_fields = ["text"]
    
    ordering_fields = ["text", "created", 'updated']
    ordering = ["updated"]
    
    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)


class GoalCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)
    


class BoardCreateView(generics.CreateAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardCreateSerializer


class BoardListView(generics.ListAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer
    
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["title"]
    
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    
    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Status.ARCHIVED)
        return instance
