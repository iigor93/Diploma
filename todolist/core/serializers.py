from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    default_error_messages = {"password_mismatch": 'password mismatch'}
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
