from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import bcrypt
from Accounts.models import studentDetails, tutorDetails, tutorSubjectDetails
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout



student = None
foundStudent = False
notfoundStudent = False

tutor = None
notfoundTutor = False
foundTutor = False

tutorDetailFetched=None
def ifLoggedIn(request):
    print(request.user.is_anonymous)
    if request.user.is_anonymous:
        return False
    else:
        return True

def encryptPassword(password):
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashedPassword.decode('utf8')


def checkPassword(password, hashedPassword):
    password = password.encode('utf-8')
    hashedPassword = hashedPassword.encode('utf-8')
    if bcrypt.checkpw(password, hashedPassword):
        return True
    else:
        return False


def home(request):
    allTutorInOurDatabase=tutorDetails.objects.all()
    isUsing = ifLoggedIn(request)
    if isUsing==False:
        return render(request, 'home_page_template/index.html', {'allTutorInOurDatabase':allTutorInOurDatabase})
    else:
        userName=request.user.username
        print(userName)
        if (userName.find(" Tutor") == -1):
            _student=studentDetails.objects.filter(emailId=request.user.email)
            for d in _student:
                student=d
            return render(request, 'home_page_template/index.html', {'foundStudent': True, 'student': student, 'allTutorInOurDatabase':allTutorInOurDatabase})
        else:
            _tutor=tutorDetails.objects.filter(emailId=request.user.email)
            for d in _tutor:
                tutor=d
            return render(request, 'home_page_template/index.html', {'foundTutor': True, 'tutor':tutor})


def studentLogin(request):
    global student, foundStudent, notfoundStudent
    # try:
    if request.method == "POST":
        foundUser=False
        userName=None
        emailId = request.POST['emailId']
        password = request.POST['password']
        detailsOfStudent = studentDetails.objects.filter(emailId=emailId)
        if len(detailsOfStudent) != 0:
            for d in detailsOfStudent:
                if checkPassword(password, d.password):
                    foundUser = True
                    student = d
                    break
        print(foundUser)
        if foundUser:
            user = authenticate(username=student.userName, password=password)
            login(request, user)
            allTutorInOurDatabase=tutorDetails.objects.all()
            foundStudent=ifLoggedIn(request)
            return render(request, 'home_page_template/index.html', {'foundStudent': foundStudent, 'student': student, 'allTutorInOurDatabase':allTutorInOurDatabase})
        else:
            return render(request, 'studentLoginTemplate/index.html', {'notfoundStudent': foundStudent})
    else:
        return render(request, 'studentLoginTemplate/index.html')
    # except:
    #     print("some error occured ")
    #     return render(request,'home_page_template/index.html')

def studentRegister(request):
    if request.method == "POST":
        fullName = request.POST['fullName']
        emailId = request.POST['emailId']
        userName = request.POST['userName']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        profilePhoto = request.FILES.get('profilePhoto', False)
        print(profilePhoto)
        if request.POST['remember-me'] == "on":
            termsAndCondition = True
        else:
            termsAndCondition = False
        if password != repeatPassword:
            messages.info(request, 'password')
            return render(request, 'studentRegisterTemplate/index.html', {'alert_flag': True})
        else:
            if studentDetails.objects.filter(emailId=emailId).exists():
                messages.info(request, 'exist')
                return render(request, 'studentLoginTemplate/index.html', {'alert_flag': True})
        studentDetails.objects.create(fullName=fullName, emailId=emailId, userName=userName,
                                      profilePhoto=profilePhoto, password=encryptPassword(password), termsAndCondition=termsAndCondition)
        user=User.objects.create_user(first_name=fullName.split()[0],last_name=fullName.split()[1:],email=emailId,username=userName,password=password)
        user.save()
        user = authenticate(username=userName, password=password)
        login(request, user)
        foundStudent=True
        detailsOfStudent = studentDetails.objects.filter(emailId=emailId)
        if len(detailsOfStudent) != 0:
            for d in detailsOfStudent:
                if checkPassword(password, d.password):
                    foundUser = True
                    student = d
                    break
        print(foundStudent)
        print(student)
        return render(request, 'home_page_template/index.html', {'foundStudent': foundStudent, 'student':student})
    else:
        return render(request, 'studentRegisterTemplate/index.html')

def tutorRegister(request):
    print("printing the request which register page is callint {}".format(request))
    if request.method == "POST":
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        emailId = request.POST['emailId']
        gender = request.POST['gender']
        profilePhoto = request.POST['profilePhoto']
        profilePhoto='tutorProfile/'+profilePhoto
        print(profilePhoto)
        if password != repeatPassword:
            messages.info(request, 'password')
            return render(request, 'tutorRegisterTemplate/index.html', {'alert_flag': True})
        else:
            if tutorDetails.objects.filter(emailId=emailId).exists():
                messages.info(request, 'exist')
                return render(request, 'tutorLoginTemplate/index.html', {'alert_flag': True})
        userName=emailId.split('@')[0]+" Tutor"
        user=User.objects.create_user(first_name=firstName, last_name=lastName, email=emailId,  username=userName, password=password)
        user.save()
        user = authenticate(username=userName, password=password)
        tutorDetails.objects.create(firstName=firstName, lastName=lastName,password=encryptPassword(password), emailId=emailId, gender=gender, profilePhoto=profilePhoto, userName=userName.split(" ")[:-1])
        detailsOftutor = tutorDetails.objects.filter(emailId=emailId)
        login(request, user)
        tutor=None
        if len(detailsOftutor) != 0:
            for d in detailsOftutor:
                if checkPassword(password, d.password):
                    foundUser = True
                    tutor = d
                    break
        foundTutor=ifLoggedIn(request)
        return render(request, 'home_page_template/index.html', {'foundTutor': foundTutor, 'tutor': tutor})
    else:
        return render(request, 'tutorRegisterTemplate/index.html')


def tutorLogin(request):
    global tutor
    print("printing the request which login page is callint {}".format(request))
    if request.method == "POST":
        emailId = request.POST['emailId']
        password = request.POST['password']
        detailsOftutor = tutorDetails.objects.filter(emailId=emailId)
        if len(detailsOftutor) != 0:
            for d in detailsOftutor:
                if checkPassword(password, d.password):
                    foundUser = True
                    tutor = d
                    break
        print(tutor)
        print(foundUser)
        userName=(emailId.split('@')[0]+" Tutor")
        if foundUser:
            user = authenticate(username=userName, password=password)
            login(request, user)
            return render(request, 'home_page_template/index.html', {'foundTutor': True, 'tutor': tutor})
        else:
            return render(request, 'tutorLoginTemplate/index.html', {'notfoundTutor': True})
    else:
        return render(request, 'tutorLoginTemplate/index.html')


def studentLogout(request):
    global student, foundStudent
    student = None
    foundStudent = False
    logout(request)
    #ifLoggedIn(request)
    return redirect('/')


def tutorLogout(request):
    global tutor, foundTutor
    tutor = None
    foundTutor = False
    logout(request)
    return redirect('/')

def detailsOfTutor(request,tutor_email):
    detailsOfTutorFetched=tutorDetails.objects.all()
    print("in details of Tutor")
    global tutorDetailFetched
    for a in detailsOfTutorFetched:
        if a.emailId==tutor_email:
            tutorDetailFetched=a
            break
    return render(request,'detailsOfTutorTemplate/index.html',{'tutorDetailFetched':tutorDetailFetched})

def tutorSubjectDetailsFilling(request):
    global tutor
    print(tutor)
    if request.method =="POST":
        subject_name1= request.POST.get('subjectName1',False)
        subject_name2= request.POST.get('subjectName2',False)
        subject_name3 = request.POST.get('subjectName3',False)
        hourlyPrice1 = request.POST.get('hourlyPrice1',False)
        hourlyPrice2 = request.POST.get('hourlyPrice2',False)
        hourlyPrice3 = request.POST.get('hourlyPrice3',False)
        address = request.POST.get('address',False)
        summary = request.POST.get('summary',False)
        phoneNumber = request.POST.get('phonenumber',False)
        print(tutor)
        print(subject_name1,subject_name2,subject_name3,hourlyPrice1,hourlyPrice2,hourlyPrice3,address,summary)
        # if subject_name1==False:
        #     subject_name1=" "
        # if subject_name2==False:
        #     subject_name2=" "
        # if subject_name3==False:
        #     subject_name3=" "
        tutorSubjectDetails.objects.create(emailId=tutor.emailId, subjectName1=subject_name1,subjectName2=subject_name2,
            subjectName3=subject_name3,hourlyPrice1=hourlyPrice1, hourlyPrice2=hourlyPrice2, hourlyPrice3=hourlyPrice3,address=address,
            phoneNumber=phoneNumber,summary=summary)
        return render(request,'home_page_template/index.html',{'foundtutor':True})
    else:
        return render(request, 'tutorSubjectDetailsTemplate/index.html')
