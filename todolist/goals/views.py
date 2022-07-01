from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant, Status
from goals.serializers import GoalCategoryCreateSerializer, GoalCategoryListSerializer, \
    GoalCreateSerializer, GoalListSerializer, GoalCommentCreateSerializer, \
    GoalCommentListSerializer, BoardCreateSerializer, BoardListSerializer, BoardSerializer
from goals.filters import GoalDateFilter

from goals.permissions import BoardPermissions, GoalCategoryCreatePermissions, \
    GoalPermissions, GoalDetailPermissions, GoalCommentCreatePermissions, GoalCommentPermissions, GoalCategoryDetailPermissions


class GoalCategoryCreateView(generics.CreateAPIView):
    """Category create"""
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated, GoalCategoryCreatePermissions]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    """category list view"""
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
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
    """category detail view"""
    model = GoalCategory
    serializer_class = GoalCategoryListSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCategoryDetailPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        current_user = request.user

        board_participant = BoardParticipant.objects.filter(user=current_user, board=instance.board).get()

        if board_participant.role == BoardParticipant.Role.OWNER or \
                board_participant.role == BoardParticipant.Role.WRITER:
            return super().update(request, *args, **kwargs)
        else:
            raise ValidationError({'Permissions': 'No permissions for this action'})

    def perform_destroy(self, instance):
        current_user = self.request.user
        
        board_participant = BoardParticipant.objects.filter(user=current_user, board=instance.board).get()
        
        if board_participant.role == BoardParticipant.Role.OWNER or \
                board_participant.role == BoardParticipant.Role.WRITER:
            instance.is_deleted = True
            instance.save()
            Goal.objects.filter(category=instance).update(status=Status.ARCHIVED, is_deleted=True)

            return instance
 
        else:
            raise ValidationError({'Permissions': 'No permissions for this action'})
        

class GoalCreateView(generics.CreateAPIView):
    """goal create view"""
    model = Goal
    permission_classes = [permissions.IsAuthenticated, GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    """goal list view"""
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
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
        return Goal.objects.select_related('category__board', 'user').filter(
            category__board__participants__user=self.request.user, is_deleted=False)


class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """goal detail view"""
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
        return Goal.objects.select_related('category__board', 'user').filter(
            category__board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.status = Status.ARCHIVED
        instance.save()
        return instance


class GoalCommentCreateView(generics.CreateAPIView):
    """comment create"""
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated, GoalCommentCreatePermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    """comment list view"""
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentListSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = ['goal']

    ordering_fields = ["text", "created", 'updated']
    ordering = ["updated"]

    def get_queryset(self):
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id)


class GoalCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """comment detail view"""
    model = GoalComment
    serializer_class = GoalCommentListSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id)


class BoardCreateView(generics.CreateAPIView):
    """board create"""
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardCreateSerializer


class BoardListView(generics.ListAPIView):
    """board list view"""
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
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
    """board detail view"""
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True) # type: ignore 
            Goal.objects.filter(category__board=instance).update(status=Status.ARCHIVED, is_deleted=True)
        return instance
