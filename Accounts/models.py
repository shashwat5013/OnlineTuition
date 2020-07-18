from django.db import models

# Create your models here.

class studentDetails(models.Model):
    fullName = models.CharField(max_length=100)
    emailId  = models.EmailField(max_length=254,primary_key=True)
    userName = models.CharField(max_length=100)
    password = models.CharField(max_length=10000)
    profilePhoto = models.ImageField(upload_to='studentProfile')
    termsAndCondition = models.BooleanField(default=False)
