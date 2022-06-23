from django.urls import path

from bot import views


urlpatterns = [
    path("verify", views.CheckVerificationCode.as_view()),
    
]
