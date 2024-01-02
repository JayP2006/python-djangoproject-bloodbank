from django.shortcuts import render,redirect
from django.db.models import Sum,Q
from . import forms,models
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from blood import models as bmodels
from blood import forms as bforms
from donor import models
from .models import Donor,BloodDonate1


# Create your views here.

def dregistration(request):
    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        mobileno=request.POST['mobileno']
        address=request.POST['address']
        username=request.POST['username']
        bloodgroup=request.POST['bloodgroup']
        password=request.POST['password']

        blood_request=User.objects.filter(username=username)
        if blood_request.exists():
            messages.error(request, "user alredy Exist!! please try some other username")
        else:  
            myuser=User.objects.create_user(username=username,password=password)
            myuser.first_name=first_name
            myuser.last_name=last_name
            blood_requests = Donor.objects.create(user=myuser,mobileno=mobileno,address=address,bloodgroup=bloodgroup
                                                        )
            myuser.save()
            blood_requests.save()
            return redirect('/dlogin')
    return render(request,'donor/d_register.html')

def dlogin(request):
    if request.method=="POST":
         username=request.POST['username']
         password=request.POST['password']

         user=authenticate(username=username,password=password)

         if user is not None:
             login(request,user)
             return redirect('/ddashboard')

         else:
            messages.error(request, "Wrong Username or password,Try again!!!.")
           
         

    return render(request,'donor/d_login.html')


@login_required(login_url='dlogin')
def ddashboard(request):
    if request.user is not None:
        
        donor= models.Donor.objects.get(user_id=request.user.id)
    
        requestpending=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Pending').count()
        requestapproved=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Approved').count()
        requestmade=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).count()
        requestrejected=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Rejected').count()
    else:
        messages.error(request, "Wrong Username or password,Try again!!!.")
    return render(request,'donor/ddashboard.html',{'requestpending':requestpending,'requestapproved':requestapproved,'requestmade':requestmade,'requestrejected':requestrejected})

@login_required(login_url='dlogin')
def dsendrequest(request):
   if request.method=="POST":
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        mobileno=request.POST['mobileno']
        address=request.POST['address']
        bloodgroup=request.POST['bloodgroup']
        unit=request.POST['unit']
        
        donor= models.Donor.objects.get(user_id=request.user.id)
        sendrequest=bmodels.BloodRequest.objects.create(request_by_donor=donor,firstname=firstname,lastname=lastname,mobileno=mobileno,address=address,bloodgroup=bloodgroup,unit=unit)
        sendrequest.save()
        return redirect('/bloodrequest_view')
   return render(request,"donor/drequest.html")

@login_required(login_url='plogin')
def dhistory(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor)
    return render(request,"donor/dstatus.html",{'blood_request':blood_request})


def donate_blood(request):
    if request.method=="POST":
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        mobileno=request.POST['mobileno']
        address=request.POST['address']
        bloodgroup=request.POST['bloodgroup']
        unit=request.POST['unit']

        donor= models.Donor.objects.get(user_id=request.user.id)
        donate_blood=BloodDonate1.objects.create(donor=donor,firstname=firstname,lastname=lastname,mobileno=mobileno,address=address,bloodgroup=bloodgroup,unit=unit)
        donate_blood.save()
        return redirect('/dbhistory')
        
    return render(request,"donor/dsendrequest.html")
def dbhistory(request):
    donor=Donor.objects.get(user_id=request.user.id)
    donations=BloodDonate1.objects.all().filter(donor=donor)
    return render(request,"donor/dbhistory.html",{'donations':donations})
def dlogout(request):
    logout(request)
    return render(request,'donor/d_login.html')

def bloodrequest_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor)
    return render(request,"donor/dstatus.html",{'blood_request':blood_request})