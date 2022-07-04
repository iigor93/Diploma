from core.models import User
from core.serializers import UserDetailSerializer

from django.db import IntegrityError
from django.db import transaction

from goals.models import Board, BoardParticipant, Goal, GoalCategory, GoalComment

from rest_framework import serializers


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = GoalCategory
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = '__all__'
        

class GoalCategoryListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
    

class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Goal
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = '__all__'
        
    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        return value


class GoalListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
        

class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = '__all__'
        

class GoalCommentListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    
    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(user=user, board=board, role=BoardParticipant.Role.OWNER)
        return board
        

class BoardListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")        
        

class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices)
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        owner = validated_data.pop("user")
        board_participant = BoardParticipant.objects.filter(user=owner, board=instance).first()
        new_participants = validated_data.pop("participants")
        
        new_by_id = {part["user"].id: part for part in new_participants}
        old_participants = instance.participants.exclude(role=BoardParticipant.Role.OWNER)
        
        if board_participant.role == BoardParticipant.Role.OWNER:
            with transaction.atomic():
                for old_participant in old_participants:
                    if old_participant.user_id not in new_by_id:
                        old_participant.delete()
                    else:
                        if old_participant.role != new_by_id[old_participant.user_id]["role"]:
                            old_participant.role = new_by_id[old_participant.user_id]["role"]
                            old_participant.save()
                            
                        new_by_id.pop(old_participant.user_id)
                        
                for new_part in new_by_id.values():
                    try:
                        BoardParticipant.objects.create(board=instance, user=new_part["user"], role=new_part["role"])
                    except IntegrityError:
                        continue

        instance.title = validated_data["title"]
        instance.save()

        return instance
