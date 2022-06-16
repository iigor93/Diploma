from rest_framework import permissions
from django.db.models import Q
from django.shortcuts import get_object_or_404

from goals.models import BoardParticipant, Board, GoalCategory, Goal


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj).exists()
        if request.method == 'DELETE':
            return BoardParticipant.objects.filter(user=request.user, board=obj, role=BoardParticipant.Role.OWNER).exists()
                                    
        return BoardParticipant.objects.filter(Q(user=request.user) & Q(board=obj) & (Q(role=BoardParticipant.Role.OWNER) | Q(role=BoardParticipant.Role.WRITER))).exists()


class GoalCategoryCreatePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        board_id = request.data.get('board')
        board = get_object_or_404(Board, pk=board_id)
        return BoardParticipant.objects.filter(Q(user=request.user) & Q(board=board) & (Q(role=BoardParticipant.Role.OWNER) | Q(role=BoardParticipant.Role.WRITER))).exists()




class GoalPermissions(permissions.BasePermission):
       def has_permission(self, request, view):
        category_id = request.data.get('category')
        category = get_object_or_404(GoalCategory, pk=category_id)
        
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(Q(user=request.user) & Q(board=category.board)).exists()

        
        return BoardParticipant.objects.filter(Q(user=request.user) & Q(board=category.board) & (Q(role=BoardParticipant.Role.OWNER) | Q(role=BoardParticipant.Role.WRITER))).exists()



class GoalDetailPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(Q(user=request.user) & Q(board=obj.category.board) ).exists()
                            
        return BoardParticipant.objects.filter(Q(user=request.user) & Q(board=obj.category.board) & (Q(role=BoardParticipant.Role.OWNER) | Q(role=BoardParticipant.Role.WRITER))).exists()


class GoalCommentCreatePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        goal_id = request.data.get('goal')
        goal = get_object_or_404(Goal, pk=goal_id)
        return BoardParticipant.objects.filter(Q(user=request.user) & Q(board=goal.category.board) & (Q(role=BoardParticipant.Role.OWNER) | Q(role=BoardParticipant.Role.WRITER))).exists()
