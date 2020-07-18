from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('studentRegister', views.studentRegister, name="studentRegister"),
    path('studentLogin', views.studentLogin, name="studentLogin"),
    path('tutorRegister',views.tutorRegister,name="tutorRegister"),
    path('tutorLogin',views.tutorLogin,name="tutorLogin")
]
