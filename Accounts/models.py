from rest_framework import serializers
from django.db import models

# Create your models here.

class studentDetails(models.Model):
    fullName          = models.CharField(max_length=100)
    emailId           = models.EmailField(max_length=254,primary_key=True)
    userName          = models.CharField(max_length=100)
    password          = models.CharField(max_length=10000)
    profilePhoto      = models.ImageField(upload_to='studentProfile',null=False)
    termsAndCondition = models.BooleanField(default=False)

    def __str__(self):
        detail=self.fullName+" "+self.emailId
        return detail


class tutorDetails(models.Model):
    firstName         = models.CharField(max_length=100)
    lastName         = models.CharField(max_length=100 , null=True)
    password         = models.CharField(max_length=10000 , null=True)
    emailId          = models.EmailField(max_length=254,primary_key=True)
    gender           = models.CharField(max_length=10, null=True)
    profilePhoto     = models.ImageField(upload_to='studentProfile', null=False)
    userName         = models.CharField(max_length=100)

    def __str__(self):
        detail=self.firstName+" "+self.lastName+" "+self.emailId
        return detail

class tutorSubjectDetails(models.Model):
    emailId           = models.EmailField(max_length=254, primary_key=True)
    subjectName1      = models.CharField(max_length=100, null=True, default=" ")
    subjectName2      = models.CharField(max_length=100, null=True, default=" ")
    subjectName3      = models.CharField(max_length=100, null=True, default=" ")
    hourlyPrice1      = models.CharField(max_length=100, null=True, default=" ")
    hourlyPrice2      = models.CharField(max_length=100, null=True, default=" ")
    hourlyPrice3      = models.CharField(max_length=100, null=True, default=" ")
    address           = models.CharField(max_length=100, null=True, default=" ")
    phoneNumber       = models.CharField(max_length=20, null=True, default=" ")
    summary           =  models.CharField(max_length=10000 , null=True, default=" ")

    def __str__(self):
        return self.emailId


class studentTutorRelation(models.Model):
    studentEmailId    = models.EmailField(max_length=254)
    tutorEmailId      = models.EmailField(max_length=254)

class tutorStudentRelation(models.Model):
    tutorEmailId      = models.EmailField(max_length=254)
    studentEmailId    = models.EmailField(max_length=254)

class tutorRequestPending(models.Model):
    tutorEmailId      = models.EmailField(max_length=254)
    studentEmailId    = models.EmailField(max_length=254)

class studentRequestFulfilled(models.Model):
    studentEmailId    = models.EmailField(max_length=254)
    tutorEmailId      = models.EmailField(max_length=254)

class studentRequestPendingPayment(models.Model):
    studentEmailId    = models.EmailField(max_length=254)
    tutorEmailId      = models.EmailField(max_length=254)

class studentRequestRejected(models.Model):
    studentEmailId    = models.EmailField(max_length=254)
    tutorEmailId      = models.EmailField(max_length=254)


class rejectedRequestSerializer(serializers.Serializer):
    firstName         = serializers.CharField(max_length=100)
    lastName         = serializers.CharField(max_length=100)
    emailId          = serializers.EmailField(max_length=254)
    profilePhoto     = serializers.ImageField()
