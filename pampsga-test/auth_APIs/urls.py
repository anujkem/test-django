from django.contrib import admin
from django.urls import path
from auth_APIs.views import *


urlpatterns = [
    path('user/registration',UserRegistration.as_view()),
    path('user/login',UserLogin.as_view()),
    path('user/logout',UserLogout.as_view()),

]