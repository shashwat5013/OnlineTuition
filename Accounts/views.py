from django.shortcuts import render,redirect
from django.http import HttpResponse
import bcrypt
from Accounts.models import studentDetails
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User,auth

# Create your views here.

def encryptPassword(password):
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    return hashedPassword.decode('utf8')


def checkPassword(password,hashedPassword):
    password=password.encode('utf-8')
    hashedPassword=hashedPassword.encode('utf-8')
    if bcrypt.checkpw(password,hashedPassword):
        return True
    else:
        return False

student=None
foundStudent = False
notfoundStudent = False
def home(request):
    print("printing the request which home page is callint {}".format(request))
    print(student)
    if student == None:
        return render(request,'home_page_template/index.html')
    else:
        return render(request,'home_page_template/index.html',{'foundStudent':True,'student':student})

def studentRegister(request):
    print("printing the request which register page is callint {}".format(request))
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
        user = User.objects.create_user(email=emailId, password = password,username=userName, first_name=fullName)
        studentDetails.objects.create(fullName=fullName,emailId=emailId,userName=userName,profilePhoto=profilePhoto,password=encryptPassword(password),termsAndCondition=termsAndCondition)
        user.save()
        return render(request,'home_page_template/index.html',{'foundStudent':True,'student':student})
    else:
        return render(request, 'studentRegisterTemplate/index.html')


def studentLogin(request):
    global student,foundStudent,notfoundStudent
    print("printing the request which login page is callint {}".format(request))
    # try:
    if request.method == "POST":
        emailId = request.POST['emailId']
        password = request.POST['password']
        detailsOfStudent = studentDetails.objects.filter(emailId=emailId)
        if len(detailsOfStudent)!=0:
            for d in detailsOfStudent:
                if checkPassword(password,d.password):
                    foundUser=True
                    student=d
                    break
        print(foundUser)
        if foundUser:
            print("authenticating user")
            user=auth.authenticate(email=emailId,password=password)
            print("loginnging in the user")
            auth.login(request,user)
            print("login done")
            return render(request,'home_page_template/index.html',{'foundStudent':True,'student':student})
        else:
            return render(request, 'studentLoginTemplate/index.html',{'notfoundStudent':True})
    else:
        return render(request, 'studentLoginTemplate/index.html')
    # except:
    #     print("some error occured ")
    #     return render(request,'home_page_template/index.html')



def tutorRegister(request):
    # user = User.objects.filter(id=2)
    # user.delete()
    return render(request,'tutorRegisterTemplate/index.html')

def tutorLogin(request):
    return render(request,'tutorLoginTemplate/index.html')

def studentLogout(request):
    auth.logout(request)
    return render(request,'home_page_template/index.html')
