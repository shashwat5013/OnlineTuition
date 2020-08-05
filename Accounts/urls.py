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
    path('',views.home,name="home"),
    path('studentLogout',views.studentLogout,name="studentLogout"),
    path('tutorLogout',views.tutorLogout,name="tutorLogout"),
    path('detailsOfTutor/<str:tutor_email>',views.detailsOfTutor,name="detailsOfTutor"),
    path('tutorSubjectDetailsFilling', views.tutorSubjectDetailsFilling, name="tutorSubjectDetailsFilling"),
]
