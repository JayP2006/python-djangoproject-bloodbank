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
from patient import models
from .models import Patient
from blood import models as bmodels


# Create your views here.
def home(request):
    x=bmodels.Stock.objects.all()
    print(x)
    if len(x)==0:
        blood1=bmodels.Stock()
        blood1.bloodgroup="A+"
        blood1.save()

        blood2=bmodels.Stock()
        blood2.bloodgroup="A-"
        blood2.save()

        blood3=bmodels.Stock()
        blood3.bloodgroup="B+"
        blood3.save()        

        blood4=bmodels.Stock()
        blood4.bloodgroup="B-"
        blood4.save()

        blood5=bmodels.Stock()
        blood5.bloodgroup="AB+"
        blood5.save()

        blood6=bmodels.Stock()
        blood6.bloodgroup="AB-"
        blood6.save()

        blood7=bmodels.Stock()
        blood7.bloodgroup="O+"
        blood7.save()

        blood8=bmodels.Stock()
        blood8.bloodgroup="O-"
        blood8.save()

    return render(request,'patient/home.html')

def registration(request):
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
            messages.error(request, "user alredy Exist!!   please try some other username")
        else:  
            myuser=User.objects.create_user(username=username,password=password)
            myuser.first_name=first_name
            myuser.last_name=last_name
            blood_requests = Patient.objects.create(user=myuser,mobileno=mobileno,address=address,bloodgroup=bloodgroup
                                                        )
            myuser.save()
            blood_requests.save()
            return redirect('/plogin')
    return render(request,'patient/register.html')

def plogin(request):
    if request.method=="POST":
         username=request.POST['username']
         password=request.POST['password']

         user=authenticate(username=username,password=password)

         if user is not None:
             login(request,user)
             fname=user.first_name
             return redirect('/pdashboard')

         else:
            messages.error(request, "Wrong Username or password,Try again!!!.")
           
         

    return render(request,'patient/login.html')


@login_required(login_url='plogin')
def pdashboard(request):
    if request.user is not None:
        messages.error(request, "successedfully login ,welcome ",request.user)
        patient= models.Patient.objects.get(user_id=request.user.id)
    
        requestpending=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Pending').count()
        requestapproved=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Approved').count()
        requestmade=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).count()
        requestrejected=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Rejected').count()
    else:
        messages.error(request, "Wrong Username or password,Try again!!!.")
    return render(request,'patient/pdashboard.html',{'requestpending':requestpending,'requestapproved':requestapproved,'requestmade':requestmade,'requestrejected':requestrejected})

@login_required(login_url='plogin')
def psendrequest(request):
   if request.method=="POST":
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        mobileno=request.POST['mobileno']
        address=request.POST['address']
        bloodgroup=request.POST['bloodgroup']
        unit=request.POST['unit']
        
        patient= models.Patient.objects.get(user_id=request.user.id)
        sendrequest=bmodels.BloodRequest.objects.create(request_by_patient=patient,firstname=firstname,lastname=lastname,mobileno=mobileno,address=address,bloodgroup=bloodgroup,unit=unit)
        sendrequest.save()
        return redirect('/phistory')
   return render(request,"patient/sendrequest.html")

@login_required(login_url='plogin')
def phistory(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient)
    return render(request,"patient/status.html",{'blood_request':blood_request})


def plogout(request):
    logout(request)
    return render(request,'patient/login.html')