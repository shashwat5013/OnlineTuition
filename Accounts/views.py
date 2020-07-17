from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def studentRegister(request):
    return render(request, 'studentRegisterTemplate/index.html')


def studentLogin(request):
    return render(request, 'studentLoginTemplate/index.html')


def tutorRegister(request):
    return render(request,'tutorRegisterTemplate/index.html')

def tutorLogin(request):
    return render(request,'tutorLoginTemplate/index.html')
