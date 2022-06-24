from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView


from bot.models import TgUser
from bot.serializers import CheckVerificationCodeSerializer
from django.core.exceptions import ObjectDoesNotExist

from bot.tg.client import TgClient
import requests

from django.conf import settings
from bot.tg import dc

# CheckVerificationCode



class CheckVerificationCode(generics.GenericAPIView):
    model = TgUser
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CheckVerificationCodeSerializer
 
    
    def patch(self, request, *args, **kwargs):

        instance = self.get_queryset()
        instance.user = request.user
        instance.save()
        tg_client = TgClient() 
        tg_client.send_message(chat_id=instance.chat_tgid, text='Verification done')
        
        return Response()
        
    def get_queryset(self): 
        verification_code = self.request.data.get('verification_code')
        try:
            return TgUser.objects.filter(verification_code=verification_code).get()
        except ObjectDoesNotExist:
            raise ValidationError({'code': 'wrong code'})
        

class TgView(APIView):
    def post(self, request, format=None):
        return Response()
