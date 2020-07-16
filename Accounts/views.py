from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def studentRegister(request):
    return render(request, 'studentRegisterTemplate/index.html')
