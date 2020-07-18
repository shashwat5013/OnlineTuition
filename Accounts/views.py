from django.shortcuts import render
from django.http import HttpResponse
import bcrypt
from Accounts.models import studentDetails
from django.contrib import messages
# Create your views here.

def encryptPassword(password):
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    return hashedPassword


def checkPassword(password,hashedPassword):
    if bcrypt.chechpw(passages,hashedPassword):
        return True
    else:
        return False


def studentRegister(request):
    if request.method =="POST":
        fullName= request.POST['fullName']
        emailId = request.POST['emailId']
        userName = request.POST['userName']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        profilePhoto=request.FILES.get('profilePhoto', False);
        if request.POST['remember-me']=="on":
            termsAndCondition = True
        else:
            termsAndCondition = False
        print(fullName,emailId,userName,password,repeatPassword,termsAndCondition,profilePhoto)
        if password!=repeatPassword:
            messages.info(request,'password')
            return render(request,'studentRegisterTemplate/index.html',{'alert_flag': True})
        else:
            if studentDetails.objects.filter(emailId=emailId).exists():
                messages.info(request,'exist')
            return render(request,'studentLoginTemplate/index.html',{'alert_flag': True})
        studentDetails.objects.create(fullName=fullName,emailId=emailId,userName=userName,profilePhoto=profilePhoto,password=encryptPassword(password),termsAndCondition=termsAndCondition)
        return render(request,'home_page_template/index.html')
    else:
        return render(request, 'studentRegisterTemplate/index.html')


def studentLogin(request):
    return render(request, 'studentLoginTemplate/index.html')


def tutorRegister(request):
    return render(request,'tutorRegisterTemplate/index.html')

def tutorLogin(request):
    return render(request,'tutorLoginTemplate/index.html')
