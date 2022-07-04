from bot.models import TgUser

from rest_framework import serializers


class CheckVerificationCodeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = TgUser
        fields = '__all__'
