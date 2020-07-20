from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('studentRegister', views.studentRegister, name="studentRegister"),
    path('studentLogin', views.studentLogin, name="studentLogin"),
    path('tutorRegister',views.tutorRegister,name="tutorRegister"),
    path('tutorLogin',views.tutorLogin,name="tutorLogin"),
    path('home',views.home,name="home"),
]
