from django.urls import path

from core import views

urlpatterns = [
    path('signup', views.UserCreate.as_view(), name='signup'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('profile', views.UserDetailView.as_view(), name='detail'),
    path('update_password', views.ChangePassword.as_view(), name='change_password'),
]
