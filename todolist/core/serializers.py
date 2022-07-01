from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """User create serializer"""
    default_error_messages = {"password_mismatch": 'Password mismatch'}
    password_repeat = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_repeat']

    def validate(self, attrs):
        self.fields.pop("password_repeat", None)
        self.fields.pop("password", None)
        re_password = attrs.pop("password_repeat")
        attrs = super().validate(attrs)
        
        validate_password(attrs['password'])
        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch")
        
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
        

class UserDetailSerializer(serializers.ModelSerializer):
    """User detail serializer"""
    class Meta:
        model = User
        read_only_fields = ['id']
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserPasswordSerializer(serializers.ModelSerializer):
    """User password serializer"""
    default_error_messages = {"wrong_old_pass": 'Wrong old password'}
    new_password = serializers.CharField()
    old_password = serializers.CharField()
    
    class Meta:
        model = User
        fields = ['new_password', 'old_password']

    def validate(self, attrs):
        self.fields.pop("new_password")
        self.fields.pop("old_password")
        attrs['password'] = attrs.pop("new_password")
        attrs = super().validate(attrs)
        
        validate_password(attrs['password'])
        return attrs
        
    def update(self, instance, validated_data):
        if instance.check_password(validated_data["old_password"]):
            instance.set_password(validated_data["password"])
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({'old_password': 'wrong old pass'})
