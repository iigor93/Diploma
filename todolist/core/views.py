import json
from rest_framework import generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


#from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django.utils.translation import gettext as _, ngettext
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from core.serializers import UserCreateSerializer, UserDetailSerializer, UserPasswordSerializer
from core.models import User



class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    

#@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserLogin(APIView):
    
    def post(self, request):
        
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
    
        if user is not None:
            login(request, user)
            serializer_ = UserDetailSerializer(user)
            return JsonResponse(serializer_.data, safe=False)
        else:
            raise serializers.ValidationError({'password': 'wrong old pass'})



#@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        user = self.request.user
        obj = get_object_or_404(queryset, pk=user.pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def delete(self, request):
        logout(request)
        return JsonResponse({'message': 'logout'}, status=204)


#@method_decorator(ensure_csrf_cookie, name='dispatch')
class ChangePassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPasswordSerializer
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        user = self.request.user
        obj = get_object_or_404(queryset, pk=user.pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
