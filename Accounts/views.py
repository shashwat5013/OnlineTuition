from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import bcrypt
from Accounts.models import studentDetails, tutorDetails, tutorSubjectDetails, tutorRequestPending, studentTutorRelation, tutorStudentRelation, studentRequestFulfilled
from Accounts.models import studentRequestRejected, studentRequestPendingPayment, rejectedRequestSerializer, teacherReview, reviewSerializer
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
import json

student = None
foundStudent = False
notfoundStudent = False

tutor = None
notfoundTutor = False
foundTutor = False

tutorDetailFetched=None
tutorEmail=None
studentEmail=None
foundUser=None
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
    print(isUsing)
    if (request.user.username=="DSANDALGO" or request.user.is_anonymous==True):
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
            tutorRequestPendingDetail=tutorRequestPending.objects.filter(tutorEmailId=request.user.email)
            pendingRequest=len(tutorRequestPendingDetail)
            print(pendingRequest)
            return render(request, 'home_page_template/index.html', {'foundTutor': True, 'tutor':tutor, 'pendingRequest':pendingRequest})

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
            #return render(request, 'home_page_template/index.html', {'foundStudent': foundStudent, 'student': student, 'allTutorInOurDatabase':allTutorInOurDatabase})
            return redirect('/')
        else:
            return render(request, 'studentLoginTemplate/index.html', {'notfoundStudent': foundStudent})
    else:
        return render(request, 'studentLoginTemplate/index.html')

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
        #return render(request, 'home_page_template/index.html', {'foundStudent': foundStudent, 'student':student})
        return redirect('/')
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
        profilePhoto='studentProfile/'+profilePhoto
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
    global tutor, foundUser
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
        # print(tutor)
        # print(foundUser)
        userName=(emailId.split('@')[0]+" Tutor")
        # print(userName)
        if foundUser:
            user = authenticate(username=userName, password=password)
            login(request, user)
            #return render(request, 'home_page_template/index.html', {'foundTutor': True, 'tutor': tutor})
            #return home(request)
            return redirect('/')
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
    global tutorEmail
    if request.user.is_anonymous:
        return redirect('/')
    if tutor_email!='album.css':
        tutorEmail=tutor_email
    detailsOfTutorFetched=tutorDetails.objects.all()
    subjectDetailsTutorFetched=tutorSubjectDetails.objects.all()
    subjectDetailsTutor=None
    tutorDetailFetched=None
    for a in detailsOfTutorFetched:
        if a.emailId==tutor_email:
            tutorDetailFetched=a
            break
    for a in subjectDetailsTutorFetched:
        if a.emailId==tutor_email:
            subjectDetailsTutor=a
            break
    fromStudentSide = True
    detailOfStudentUnder=[]
    if request.user.username.find(" Tutor")!=-1:
        fromStudentSide=False
    if fromStudentSide==True or fromStudentSide==False:
        studentUnder=tutorStudentRelation.objects.filter(tutorEmailId=request.user.email)
        for i in range(len(studentUnder)):
            studentEmail=studentUnder[i].studentEmailId
            print(studentEmail)
            studentDB=studentDetails.objects.filter(emailId=studentEmail)
            for j in range(len(studentDB)):
                detailOfStudentUnder.append(studentDB[i])
    hisStudent=False
    if fromStudentSide==True:
        studentEmail=request.user.email
        if tutorStudentRelation.objects.filter(tutorEmailId=tutorEmail,studentEmailId=studentEmail).exists():
            hisStudent=True
    reviewDB=teacherReview.objects.filter(tutorEmailId=tutorEmail)
    print(reviewDB)
    reviewDetails=list()
    for rr in reviewDB:
        print(reviewDetails.append(rr))
    numberOfReviews=len(reviewDB)
    noReview=True
    if numberOfReviews==0:
        noReview=False
    print(reviewDetails)
    noStudent=True
    if len(detailOfStudentUnder)==0:
        noStudent=False
    print("accessing tutorDetail")
    return render(request,'detailsOfTutorTemplate/index.html',{'noReview':noReview,'noStudent':noStudent,'detailOfStudentUnder':detailOfStudentUnder,'fromStudentSide':fromStudentSide,'tutorDetailFetched':tutorDetailFetched, 'subjectDetailsTutor':subjectDetailsTutor,'hisStudent':hisStudent,'reviewDetails':reviewDetails})

def tutorSubjectDetailsFilling(request):
    tutor=None
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
        tutorSubjectDetails.objects.create(emailId=request.user.email, subjectName1=subject_name1,subjectName2=subject_name2,
            subjectName3=subject_name3,hourlyPrice1=hourlyPrice1, hourlyPrice2=hourlyPrice2, hourlyPrice3=hourlyPrice3,address=address,
            phoneNumber=phoneNumber,summary=summary)
        return render(request,'home_page_template/index.html',{'foundtutor':True})
    else:
        return render(request, 'tutorSubjectDetailsTemplate/index.html')

def tutorRequestPendingUrl(request,tutor_email):
    if request.user.is_anonymous==True:
        return render(request,'studentLoginTemplate/index.html')
    studentEmail= request.user.email
    tutorEmail = tutor_email
    tutorRequestPendingDetail= tutorRequestPending.objects.filter(tutorEmailId=tutorEmail)
    for i in range(len(tutorRequestPendingDetail)):
        if tutorRequestPendingDetail[i].tutorEmailId==tutorEmail and tutorRequestPendingDetail[i].studentEmailId==studentEmail:
            print('already exists')
            return home(request)
    tutorRequestPending.objects.create(tutorEmailId=tutorEmail, studentEmailId=studentEmail)
    return home(request)

def pendingRequest(request):
    studentEmails=tutorRequestPending.objects.filter(tutorEmailId=request.user.email)
    studentUnderYou=[]
    for i  in range(len(studentEmails)):
        studentEmail=studentEmails[i].studentEmailId
        ss=studentDetails.objects.filter(emailId=studentEmail)
        for j in range(len(ss)):
            studentUnderYou.append(ss[j])
    isPending=False
    if len(studentUnderYou)!=0:
        isPending=True
    # if isPending==False:
    #     return render(request,'demo.html')
    # else:
    return render(request,'studentPendingRequestTemplate/index.html',{'studentUnderYou':studentUnderYou,'isPending':isPending})

def accepting(request,student_emailId):
    print(student_emailId)
    tutor_email=request.user.email
    if student_emailId!='album.css':
        tutorRequestPending.objects.filter(tutorEmailId=tutor_email,studentEmailId=student_emailId).delete()
        checkStudent=studentTutorRelation.objects.filter(studentEmailId=student_emailId)
        for s in checkStudent:
            if s.tutorEmailId==tutor_email:
                return pendingRequest(request)
        checkTutor=tutorStudentRelation.objects.filter(tutorEmailId=tutor_email)
        for s in checkTutor:
            if s.studentEmailId==student_emailId:
                return pendingRequest(request)
        studentTutorRelation.objects.create(tutorEmailId=tutor_email,studentEmailId=student_emailId)
        tutorStudentRelation.objects.create(tutorEmailId=tutor_email,studentEmailId=student_emailId)
        studentRequestPendingPayment.objects.create(studentEmailId=student_emailId,tutorEmailId=tutor_email)
    return pendingRequest(request)

def rejecting(request,student_emailId):
    global tutorEmail
    tutorEmail=request.user.email
    if student_emailId!='album.css':
        studentRequestRejected.objects.create(studentEmailId=student_emailId,tutorEmailId=tutorEmail)
        tutorRequestPending.objects.filter(tutorEmailId=tutorEmail,studentEmailId=student_emailId).delete()
    return pendingRequest(request)

def studentDetailUrl(request,student_emailId):
    global studentEmail
    if student_emailId!='album.css':
        studentEmail=student_emailId
        print(studentEmail)
    studentDetailsDB=studentDetails.objects.filter(emailId=studentEmail)
    studentDetailFetched=None
    for i in range(len(studentDetailsDB)):
        studentDetailFetched=studentDetailsDB[i]
        break
    detailOfTutorUnder=[]
    studentTutorDB=studentTutorRelation.objects.filter(studentEmailId=studentEmail)
    for i in range(len(studentTutorDB)):
        tutorEmail=studentTutorDB[i].tutorEmailId
        tutorDB=tutorDetails.objects.filter(emailId=tutorEmail)
        for j in range(len(tutorDB)):
            detailOfTutorUnder.append(tutorDB[j])
    print("printing data")
    print(studentDetailFetched.profilePhoto.url)
    print(detailOfTutorUnder)
    return render(request,'detailsOfStudentTemplate/index.html',{'detailOfTutorUnder':detailOfTutorUnder,'fromStudentSide':False,'studentDetailFetched':studentDetailFetched})

def requestStatusUrl(request):
    studentEmail=request.user.email
    print(studentEmail)
    pendingRequestDB=tutorRequestPending.objects.filter(studentEmailId=studentEmail)
    #print(pendingRequestDB)
    pendingRequestDetails=[]
    for pending in pendingRequestDB:
        if pending.studentEmailId==studentEmail:
            data=tutorDetails.objects.filter(emailId=pending.tutorEmailId)
            for d in data:
                pendingRequestDetails.append(d)
    print(pendingRequestDetails)
    return render(request,'studentRequestStatusTemplate/index.html',{'pendingRequestDetails':pendingRequestDetails})

def studentPendingRequestUrl(request):
    studentEmail=request.user.email
    studentRejectedDB=tutorRequestPending.objects.filter(studentEmailId=studentEmail)
    print("data")
    print(studentRejectedDB)
    studentRequestRejectedDetails=list()
    for rejected in studentRejectedDB:
        dataa=tutorDetails.objects.filter(emailId=rejected.tutorEmailId)
        for d in dataa:
            ser=rejectedRequestSerializer(d)
            studentRequestRejectedDetails.append(ser.data)
    studentRequestRejectedDetails=json.dumps(studentRequestRejectedDetails)
    print(studentRequestRejectedDetails)
    return HttpResponse(studentRequestRejectedDetails)

def studentRequestRejectedUrl(request):
    studentEmail=request.user.email
    studentRejectedDB=studentRequestRejected.objects.filter(studentEmailId=studentEmail)
    studentRequestRejectedDetails=list()
    for rejected in studentRejectedDB:
        dataa=tutorDetails.objects.filter(emailId=rejected.tutorEmailId)
        for d in dataa:
            ser=rejectedRequestSerializer(d)
            studentRequestRejectedDetails.append(ser.data)
    studentRequestRejectedDetails=json.dumps(studentRequestRejectedDetails)
    return HttpResponse(studentRequestRejectedDetails)

def studentRequestPendingPaymentUrl(request):
    studentEmail=request.user.email
    studentRejectedDB=studentRequestPendingPayment.objects.filter(studentEmailId=studentEmail)
    studentRequestPendingPaymentDetails=list()
    for rejected in studentRejectedDB:
        dataa=tutorDetails.objects.filter(emailId=rejected.tutorEmailId)
        for d in dataa:
            ser=rejectedRequestSerializer(d)
            studentRequestPendingPaymentDetails.append(ser.data)
    studentRequestPendingPaymentDetails=json.dumps(studentRequestPendingPaymentDetails)
    print(studentRequestPendingPaymentDetails)
    return HttpResponse(studentRequestPendingPaymentDetails)

def reviewSentimentAnalysis(request):
    review=request.GET['review']
    print(review);
    class reviewAnalysis:
        def reviewSentimentAnalysisFunction(self,review):
            import re
            import nltk
            import  pickle
            from nltk.corpus import stopwords
            from nltk.stem.porter import PorterStemmer
            ps = PorterStemmer()
            corpus = []

            filename = 'C:/Users/shash/Desktop/Data_Science/dataScience/SentimentAnalysis/nlp_model.pkl'
            clf = pickle.load(open(filename, 'rb'))
            vectorizer = pickle.load(open('C:/Users/shash/Desktop/Data_Science/dataScience/SentimentAnalysis/tranform.pkl','rb'))

            m=list()
            m.append(review)
            c=[]
            for i in range(0, len(m)):
                review = re.sub('[^a-zA-Z]', ' ', m[i])
                review = review.lower()
                review = review.split()
                review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
                review = ' '.join(review)
                c.append(review)

            X_user = vectorizer.transform(c).toarray()
            y_user=clf.predict(X_user)
            if y_user==1:
                return 1
            else:
                return 0
    r=reviewAnalysis()
    val=r.reviewSentimentAnalysisFunction(review);
    if val==0:
        rr=False
    else:
        rr=True
    if request.user.email!="album.css":
        teacherReview.objects.create(studentEmailId=request.user.email,tutorEmailId=request.GET['tutor_email'],review=review,points=val,numberOfReviews=rr);
    reviewDB=teacherReview.objects.filter(studentEmailId=request.user.email)
    print(reviewDB)
    reviewDetails=list()
    for rejected in reviewDB:
        ser=reviewSerializer(rejected)
        reviewDetails.append(ser.data)
    reviewDetails=json.dumps(reviewDetails)
    print(reviewDetails)
    return HttpResponse(reviewDetails)
