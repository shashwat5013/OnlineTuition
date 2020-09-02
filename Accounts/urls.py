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
    path('tutorRequestPendingUrl/<str:tutor_email>',views.tutorRequestPendingUrl, name="tutorRequestPendingUrl"),
    path('pendingRequest',views.pendingRequest, name= 'pendingRequest'),
    path('accepting/<str:student_emailId>',views.accepting, name='accepting'),
    path('rejecting/<str:student_emailId>',views.rejecting, name='rejecting'),
    path('studentDetailUrl/<str:student_emailId>',views.studentDetailUrl, name='studentDetailUrl'),
    path('requestStatusUrl',views.requestStatusUrl, name='requestStatusUrl'),
    path('studentRequestRejectedUrl', views.studentRequestRejectedUrl,name='studentRequestRejectedUrl'),
    path('studentRequestPendingPaymentUrl', views.studentRequestPendingPaymentUrl,name='studentRequestPendingPaymentUrl'),
    path('studentPendingRequestUrl', views.studentPendingRequestUrl,name='studentPendingRequestUrl'),
    path('reviewSentimentAnalysis', views.reviewSentimentAnalysis,name='reviewSentimentAnalysis'),
    path('tutorAlreadyFilledDetail',views.tutorAlreadyFilledDetail,name='tutorAlreadyFilledDetail'),
]
