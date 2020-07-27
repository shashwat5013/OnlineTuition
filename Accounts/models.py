from django.db import models
# Create your models here.

class studentDetails(models.Model):
    fullName          = models.CharField(max_length=100)
    emailId           = models.EmailField(max_length=254,primary_key=True)
    userName          = models.CharField(max_length=100)
    password          = models.CharField(max_length=10000)
    profilePhoto      = models.ImageField(upload_to='studentProfile')
    termsAndCondition = models.BooleanField(default=False)
      

class tutorDetails(models.Model):
    fullName         = models.CharField(max_length=100)
    emailId          = models.EmailField(max_length=254,primary_key=True)
    gender           = models.CharField(max_length=10)
    mobileNumber     = models.CharField(max_length=20)
    specialityCourse = models.CharField(max_length=50)
    profilePhoto     = models.ImageField(upload_to='tutorProfile')
