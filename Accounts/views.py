from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import bcrypt
from Accounts.models import studentDetails, tutorDetails, tutorSubjectDetails, tutorRequestPending, studentTutorRelation, tutorStudentRelation, studentRequestFulfilled
from Accounts.models import studentRequestRejected, studentRequestPendingPayment, rejectedRequestSerializer, teacherReview, reviewSerializer
from Accounts.models import tutorSubjectSerializer,newStudentTable, newTutorTable
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
import json
from django.views.decorators.csrf import csrf_exempt
from payTm import Checksum
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

alert_flag=None
MERCHANT_KEY=''
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
    global alert_flag
    allTutorInOurDatabase=tutorDetails.objects.all()
    isUsing = ifLoggedIn(request)
    print(isUsing)
    if (request.user.username=="DSANDALGO" or request.user.is_anonymous==True):
        return render(request, 'home_page_template/index.html', {'allTutorInOurDatabase':allTutorInOurDatabase,'no_user':True})
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


def studentRegister(request,DfullName,DemailId,Dpassword,DprofilePhoto,Dgender):
    fullName = DfullName
    emailId = DemailId
    password = Dpassword
    userName=fullName
    profilePhoto = DprofilePhoto
    termsAndCondition=True
    newStudentTable.objects.create(fullName=fullName,emailId=emailId,password=encryptPassword(password),gender=Dgender,profilePhoto=profilePhoto)
    studentDetails.objects.create(fullName=fullName, emailId=emailId, userName=userName,
                                  profilePhoto=profilePhoto, password=encryptPassword(password), termsAndCondition=termsAndCondition,gender=Dgender)
    user=User.objects.create_user(first_name=fullName,email=emailId,username=userName,password=password)
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


def tutorRegister(request,DfullName,DemailId,Dpassword,DprofilePhoto,Dgender):
    print("printing the request which register page is callint {}".format(request))
    firstName = DfullName
    lastName = DfullName
    password = Dpassword
    emailId = DemailId
    gender = Dgender
    profilePhoto = DprofilePhoto
    print(profilePhoto)
    userName=emailId.split('@')[0]+" Tutor"
    user=User.objects.create_user(first_name=firstName, last_name=lastName, email=emailId,  username=userName, password=password)
    user.save()
    user = authenticate(username=userName, password=password)
    newTutorTable.objects.create(fullName=DfullName,emailId=DemailId,password=encryptPassword(Dpassword),profilePhoto=DprofilePhoto,gender=Dgender)
    tutorDetails.objects.create(firstName=firstName, lastName=lastName,password=encryptPassword(password), emailId=emailId, gender=gender, profilePhoto=profilePhoto, userName=userName.split(" ")[:-1])
    detailsOftutor = tutorDetails.objects.filter(emailId=emailId)
    print(detailsOfTutor)
    login(request, user)
    tutor=None
    if len(detailsOftutor) != 0:
        for d in detailsOftutor:
            if checkPassword(password, d.password):
                foundUser = True
                tutor = d
                break
    foundTutor=ifLoggedIn(request)
    return redirect('/')


def Register(request):
    fullName=request.POST['Username']
    emailId=request.POST['EmailId']
    password=request.POST['Password']
    repeatPassword=request.POST['ConfirmPassword']
    profilePhoto=request.FILES.get('ProfileImage',False)
    gender=request.POST['gender']
    designation=request.POST['designation']
    print(fullName,emailId,password,repeatPassword,profilePhoto,gender,designation)
    if password!=repeatPassword:
        return render('home_page_template/index.html',{'alert_flag':True})
    if designation=='student':
        return studentRegister(request,fullName,emailId,password,profilePhoto,gender)
    else:
        return tutorRegister(request,fullName,emailId,password,profilePhoto,gender)

def tutorLogin(request,DemailId,Dpassword):
    global tutor, foundUser,alert_flag
    emailId = DemailId
    password = Dpassword
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
        alert_flag=False
        return redirect('/')
    else:
        alert_flag=True
        return redirect('/')

def studentLogin(request,DemailId,Dpassword):
    global student, foundStudent, notfoundStudent, alert_flag
    foundUser=False
    userName=None
    emailId = DemailId
    password = Dpassword
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
        alert_flag=False
        return redirect('/')
    else:
        alert_flag=True
        return redirect('/')

def Login(request):
    emailId=request.POST['EmailId']
    password=request.POST['Password']
    designation=request.POST['designation']
    print(emailId,password,designation)
    if(designation=="student"):
        return studentLogin(request,emailId,password)
    else:
        return tutorLogin(request,emailId,password)


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
    print('in detail fo tutor')
    global tutorEmail
    if request.user.is_anonymous:
        return redirect('/')
    if tutor_email!='album.css':
        tutorEmail=tutor_email
    detailsOfTutorFetched=tutorDetails.objects.all()
    subjectDetailsTutorFetched=tutorSubjectDetails.objects.all()
    print(subjectDetailsTutorFetched)
    subjectDetailsTutor=list()
    tutorDetailFetched=None
    for a in detailsOfTutorFetched:
        if a.emailId==tutorEmail:
            tutorDetailFetched=a
            break
    for a in subjectDetailsTutorFetched:
        if a.emailId==tutorEmail:
            subjectDetailsTutor.append(a)
            break
    print(subjectDetailsTutor)
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
                detailOfStudentUnder.append(studentDB[j])
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
    noStudent=True
    if len(detailOfStudentUnder)==0:
        noStudent=False
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
        print(tutorSubjectDetails.objects.filter(emailId=request.user.email).exists())
        if tutorSubjectDetails.objects.filter(emailId=request.user.email).exists():
                tutorSubjectDetails.objects.filter(emailId=request.user.email).delete()
        tutorSubjectDetails.objects.create(emailId=request.user.email, subjectName1=subject_name1,subjectName2=subject_name2,
            subjectName3=subject_name3,hourlyPrice1=hourlyPrice1, hourlyPrice2=hourlyPrice2, hourlyPrice3=hourlyPrice3,address=address,
            phoneNumber=phoneNumber,summary=summary)
        return redirect('/')
    else:
        return render(request, 'tutorSubjectDetailsTemplate/index.html')

def tutorRequestPendingUrl(request,tutor_email):
    studentEmail= request.user.email
    global tutorEmail
    if tutorEmail!='album.css':
        tutorEmail=tutor_email
    subject=""
    subject=request.POST['cars']
    print(subject)
    tutorEmail = tutor_email
    tutorRequestPendingDetail= tutorRequestPending.objects.filter(tutorEmailId=tutorEmail)
    for i in range(len(tutorRequestPendingDetail)):
        if tutorRequestPendingDetail[i].tutorEmailId==tutorEmail and tutorRequestPendingDetail[i].studentEmailId==studentEmail and tutorRequestPendingDetail[i].subject==subject:
            print('already exists')
            return home(request)
    tutorRequestPending.objects.create(tutorEmailId=tutorEmail, studentEmailId=studentEmail,subject=subject)
    return home(request)

def pendingRequest(request):
    class tutorRequestClass:
        def __init__(self,id,fullName,emailId,userName,profilePhoto,subject):
            self.id=id
            self.fullName=fullName
            self.emailId=emailId
            self.userName=userName
            self.profilePhoto=profilePhoto
            self.subject=subject
    studentEmails=tutorRequestPending.objects.filter(tutorEmailId=request.user.email)
    studentUnderYou=[]
    ids=list()
    for i  in range(len(studentEmails)):
        studentEmail=studentEmails[i].studentEmailId
        ids.append(studentEmails[i].id)
        print(ids)
        ss=studentDetails.objects.filter(emailId=studentEmail)
        for j in range(len(ss)):
            a=tutorRequestClass(studentEmails[i].id,ss[j].fullName,ss[j].emailId,ss[j].userName,ss[j].profilePhoto,studentEmails[i].subject)
            studentUnderYou.append(a)
    print("pending Request")
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
        print("adding accepting status")
        tu=tutorRequestPending.objects.filter(studentEmailId=student_emailId,tutorEmailId=request.user.email,subject=request.GET['subject'])
        print(tu)
        print(student_emailId,request.user.email,request.GET['subject'])
        tutorRequestPending.objects.filter(studentEmailId=student_emailId,tutorEmailId=request.user.email,subject=request.GET['subject']).delete()
        id=None
        studnetD=None
        tutorD=None
        subjectD=None
        for t in tu:
            id=t.id
            studentD=t.studentEmailId
            tutorD=t.tutorEmailId
            subjectD=t.subject
        if studentTutorRelation.objects.filter(studentEmailId=student_emailId,tutorEmailId=request.user.email,subject=request.GET['subject']).exists()==False and tutorStudentRelation.objects.filter(studentEmailId=student_emailId,tutorEmailId=request.user.email,subject=request.GET['subject']).exists()==False:
            if studentRequestPendingPayment.objects.filter(studentEmailId=student_emailId,tutorEmailId=request.user.email,subject=request.GET['subject']).exists()==False:
                studentRequestPendingPayment.objects.create(studentEmailId=student_emailId,tutorEmailId=request.user.email,subject=request.GET['subject'])
    return pendingRequest(request)
        # checkStudent=studentTutorRelation.objects.filter(studentEmailId=studnetD)
        # for s in checkStudent:
        #     if s.tutorEmailId==tutor_email:
        #         return pendingRequest(request)
        # checkTutor=tutorStudentRelation.objects.filter(tutorEmailId=tutorD)
        # for s in checkTutor:
        #     if s.studentEmailId==student_emailId:
        #         return pendingRequest(request)

def rejecting(request,student_emailId):
    global tutorEmail
    tutorEmail=request.user.email
    if student_emailId!='album.css':
        studentRequestRejected.objects.create(studentEmailId=student_emailId,tutorEmailId=request.user.email,subject=request.GET['subject'])
        tutorRequestPending.objects.filter(studentEmailId=student_emailId,tutorEmailId=request.user.email,subject=request.GET['subject']).delete()
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
    class forSerializer:
        def __init__(self,id,firstName,emailId,profilePhoto,subject):
            self.id=id
            self.firstName=firstName
            self.lastName=""
            self.emailId=emailId
            self.profilePhoto=profilePhoto
            self.subject=subject
    studentEmail=request.user.email
    studentRejectedDB=tutorRequestPending.objects.filter(studentEmailId=studentEmail)
    print("data")
    print(studentRejectedDB)
    studentRequestRejectedDetails=list()
    for rejected in studentRejectedDB:
        print(rejected.id)
        dataa=tutorDetails.objects.filter(emailId=rejected.tutorEmailId)
        for d in dataa:
            dd=forSerializer(rejected.id,d.firstName,d.emailId,d.profilePhoto,rejected.subject)
            ser=rejectedRequestSerializer(dd)
            studentRequestRejectedDetails.append(ser.data)
    studentRequestRejectedDetails=json.dumps(studentRequestRejectedDetails)
    print(studentRequestRejectedDetails)
    return HttpResponse(studentRequestRejectedDetails)


def studentRequestRejectedUrl(request):
    class forSerializer:
        def __init__(self,id,firstName,emailId,profilePhoto,subject):
            self.id=id
            self.firstName=firstName
            self.lastName=""
            self.emailId=emailId
            self.profilePhoto=profilePhoto
            self.subject=subject
    studentEmail=request.user.email
    studentRejectedDB=studentRequestRejected.objects.filter(studentEmailId=studentEmail)
    studentRequestRejectedDetails=list()
    for rejected in studentRejectedDB:
        dataa=tutorDetails.objects.filter(emailId=rejected.tutorEmailId)
        for d in dataa:
            dd=forSerializer(rejected.id,d.firstName,d.emailId,d.profilePhoto,rejected.subject)
            ser=rejectedRequestSerializer(dd)
            studentRequestRejectedDetails.append(ser.data)
    studentRequestRejectedDetails=json.dumps(studentRequestRejectedDetails)
    return HttpResponse(studentRequestRejectedDetails)


def studentRequestPendingPaymentUrl(request):
    class forSerializer:
        def __init__(self,id,firstName,emailId,profilePhoto,subject):
            self.id=id
            self.firstName=firstName
            self.lastName=""
            self.emailId=emailId
            self.profilePhoto=profilePhoto
            self.subject=subject
    studentEmail=request.user.email
    print(studentEmail)
    studentRejectedDB=studentRequestPendingPayment.objects.filter(studentEmailId=studentEmail)
    print(studentRejectedDB)
    studentRequestPendingPaymentDetails=list()
    for rejected in studentRejectedDB:
        dataa=tutorDetails.objects.filter(emailId=rejected.tutorEmailId)
        for d in dataa:
            dd=forSerializer(rejected.id,d.firstName,d.emailId,d.profilePhoto,rejected.subject)
            ser=rejectedRequestSerializer(dd)
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
            nltk.download('stopwords')
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
    reviewDB=teacherReview.objects.filter(studentEmailId=request.user.email,tutorEmailId=request.GET['tutor_email'])
    print(reviewDB)
    reviewDetails=list()
    for rejected in reviewDB:
        ser=reviewSerializer(rejected)
        reviewDetails.append(ser.data)
    reviewDetails=json.dumps(reviewDetails)
    print(reviewDetails)
    return HttpResponse(reviewDetails)

def tutorAlreadyFilledDetail(request):
    if request.user.email!='album.css':
        if tutorSubjectDetails.objects.filter(emailId=request.user.email).exists():
            tutorSubjectDB=tutorSubjectDetails.objects.filter(emailId=request.user.email)
            tutorSubjectDetail=list()
            for t in tutorSubjectDB:
                tutorSubjectDetail.append(tutorSubjectSerializer(t).data)
            tutorSubjectDetail=json.dumps(tutorSubjectDetail)
            print(tutorSubjectDetail)
            return HttpResponse(tutorSubjectDetail)
        else:
            return HttpResponse('false')
    else:
        return HttpResponse('false')


def pleaseMakePayment(request,tutor_email):
    detailTutorDB=None
    subjectDetailDB=None
    detailTutor=list()
    cost=None
    if tutor_email!='album.css':
        subject=request.GET['subject']
        detailTutorDB=tutorDetails.objects.filter(emailId=tutor_email);
        subjectDetailDB=tutorSubjectDetails.objects.filter(emailId=tutor_email)
        for d in detailTutorDB:
            detailTutor.append(d)
        for d in subjectDetailDB:
            if d.subjectName1.lower()==subject.lower():
                cost=d.hourlyPrice1
            elif d.subjectName2.lower()==subject.lower():
                cost=d.hourlyPrice2
            elif d.subjectName3.lower()==subject.lower():
                cost=d.hourlyPrice2
        print(cost,subject)
    return render(request,'demo.html',{'detailTutor':detailTutor,'cost':cost,'subject':subject,'tutor_emailId':tutor_email})
    # print(studentRequestPendingPayment.objects.all())
    # studentRequestPendingPayment.objects.filter(studentEmailId=request.user.email,tutorEmailId=tutor_email,subject=request.GET['subject']).delete()
    # print(studentRequestPendingPayment.objects.all())
    # if studentRequestFulfilled.objects.filter(studentEmailId=request.user.email,tutorEmailId=tutor_email,subject=request.GET['subject']).exists()==False:
    #     studentRequestFulfilled.objects.create(studentEmailId=request.user.email,tutorEmailId=tutor_email,subject=request.GET['subject'])
    #     studentTutorRelation.objects.create(studentEmailId=request.user.email,tutorEmailId=tutor_email,subject=request.GET['subject'])
    #     tutorStudentRelation.objects.create(tutorEmailId=tutor_email,studentEmailId=request.user.email,subject=request.GET['subject'])
    # ans=""
    # ans+=request.user.email+" "+tutor_email+" "+request.GET['subject']
    # return HttpResponse(ans)
def handlingPaymentRequestSender(request):
    tutor_email=request.POST['emailId']
    # subject=request.POST['subject']
    subjects=request.POST['subject']
    cost=request.POST['cost']
    if tutor_email!='album.css':
        print(tutor_email,subjects,cost)
        if studentRequestPendingPayment.objects.filter(studentEmailId=request.user.email,tutorEmailId=tutor_email,subject=subjects).exists():
            aa=studentRequestPendingPayment.objects.filter(studentEmailId=request.user.email,tutorEmailId=tutor_email,subject=subjects)
            order_id=None
            for a in aa:
                print(a.id)
                order_id=a.id
                new_oder_id=str(order_id)+"@@"+subjects+"@@"+tutor_email+"@@"+request.user.email
                param_dict={
                'MID': '',
                'ORDER_ID': str(new_oder_id),
                'TXN_AMOUNT': str(cost),
                'CUST_ID': tutor_email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/Accounts/handlerequest/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request,'paytm.html',{'param_dict':param_dict})
        else:
            return redirect('/')
@csrf_exempt
def handlerequest(request):
    #paytm will send post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        response_dict['RESPCODE'] ='01'
        # if response_dict['RESPCODE'] == '01':
        print('order successful')
        tutor_email=response_dict['ORDERID'].split('@@')[2]
        subjects=response_dict['ORDERID'].split('@@')[1]
        student_email=response_dict['ORDERID'].split('@@')[3]
        studentRequestPendingPayment.objects.filter(studentEmailId=student_email,tutorEmailId=tutor_email,subject=subjects).delete()
        studentTutorRelation.objects.create(studentEmailId=student_email,tutorEmailId=tutor_email,subject=subjects)
        tutorStudentRelation.objects.create(tutorEmailId=tutor_email,studentEmailId=student_email,subject=subjects)
        studentRequestFulfilled.objects.create(studentEmailId=student_email,tutorEmailId=tutor_email,subject=subjects)
        # else:
            # print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})
