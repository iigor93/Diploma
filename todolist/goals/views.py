from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from goals.models import GoalCategory, Goal, GoalComment
from goals.serializers import GoalCategoryCreateSerializer, GoalCategoryListSerializer, GoalCreateSerializer, GoalListSerializer
from goals.serializers import GoalCommentCreateSerializer, GoalCommentListSerializer
from goals.filters import GoalDateFilter





class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer
    

class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    prmission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryListSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = ["title"]
    
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    
    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)
        

class GoalCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)
    
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    prmission_classes = [permissions.IsAuthenticated]
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
        return Goal.objects.filter(user=self.request.user, is_deleted=False)


class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user, is_deleted=False)
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
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
    
