from django.urls import path

from bot import views


urlpatterns = [
    path("verify", views.CheckVerificationCode.as_view()),
    path('AAFsxiOtOD1dyyttS48T2Ni7nwmaHK36kVg', views.TgView.as_view()),
]
