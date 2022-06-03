from django.urls import path

from core import views

urlpatterns = [
    path('signup/', views.UserCreate.as_view(), name='signup'),
]
