from django.shortcuts import render
from django.http import HttpResponse
from Accounts.models import tutorDetails
# Create your views here.


def home(request):
    allTutorInOurDatabase=tutorDetails.objects.all()
    return render(request, "home_page_template\index.html",{'allTutorInOurDatabase':allTutorInOurDatabase})
