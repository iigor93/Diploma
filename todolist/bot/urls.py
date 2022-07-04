from bot import views

from django.urls import path


urlpatterns = [
    path("verify", views.CheckVerificationCode.as_view()),
]
