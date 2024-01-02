from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from patient  import models as pmodels
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from donor import models as dmodels
from .models import Stock,BloodRequest


def admin_login(request):
      if request.method=="POST":
         username=request.POST['username']
         password=request.POST['password']

         user=authenticate(username=username,password=password)

         if user is not None:
             login(request,user)
             return redirect('/admin_dashboard')

         else:
            messages.error(request, "Wrong Username or password,Try again!!!.")
      return render(request,'action/alogin.html')


def admin_dashboard(request):
    A1 = Stock.objects.get(bloodgroup="A+")
    B1 = Stock.objects.get(bloodgroup="B+")
    A2 = Stock.objects.get(bloodgroup="A-")
    B2 = Stock.objects.get(bloodgroup="B-")
    AB1 = Stock.objects.get(bloodgroup="AB+")
    AB2 = Stock.objects.get(bloodgroup="AB-")
    O1 = Stock.objects.get(bloodgroup="O+")
    O2 = Stock.objects.get(bloodgroup="O-")
    donors=dmodels.Donor.objects.all().count()
    requests=BloodRequest.objects.all().count()
    approved = BloodRequest.objects.filter(status='Approved').count()
    totalunit = Stock.objects.aggregate(Sum('unit'))
    totalbloodunit=totalunit['unit__sum']
    return render(request,"action/addashboard.html",{'donors':donors,'requests':requests,'approved':approved,'totalbloodunit':totalbloodunit,'A1':A1,'B1':B1,'A2':A2,'B2':B2,'AB1':AB1,'AB2':AB2,'O1':O1,'O2':O2})

def updatep(request,id):
    patient=pmodels.Patient.objects.get(pk=id)
    user=pmodels.User.objects.get(id=patient.user_id)
    if request.method=="POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        mobileno = request.POST['mobileno']
        address = request.POST['address']
        bloodgroup = request.POST['bloodgroup']

        p=pmodels.Patient.objects.get(pk=id)
        u=user=pmodels.User.objects.get(id=patient.user_id)
        u.first_name=firstname
        u.last_name=lastname    
        p.mobileno=mobileno
        p.address=address
        p.bloodgroup=bloodgroup

        u.save()
        p.save()
        messages.success(request, "Patients details are Successfully updated")
        return redirect('/p_admin')
    return render(request,"action/updatep.html",{'patient':patient})

def updated(request,id):
     donor=dmodels.Donor.objects.get(pk=id)
     user=dmodels.User.objects.get(id=donor.user_id)
     if request.method=="POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        mobileno = request.POST['mobileno']
        address = request.POST['address']
        bloodgroup = request.POST['bloodgroup']

        p=dmodels.Donor.objects.get(pk=id)
        u=user=pmodels.User.objects.get(id=donor.user_id)
        u.first_name=firstname
        u.last_name=lastname    
        p.mobileno=mobileno
        p.address=address
        p.bloodgroup=bloodgroup

        u.save()
        p.save()
        messages.success(request, "Donors details are Successfully updated")
        return redirect('/d_admin')
     return render(request,"action/updated.html",{'donor':donor})

def deletep(request,id):
    if request.user is not None:
        patient=pmodels.Patient.objects.get(pk=id)
        patient.delete()
        messages.success(request, "user successfuly deleted")
        return redirect('/p_admin')
    else:
          messages.error(request, "error.")
    return render(request,"action/p_admin.html")

def deleted(request,id):
    if request.user is not None:
        donor=dmodels.Donor.objects.get(pk=id)
        donor.delete()
        messages.success(request, "user successfuly deleted")
        return redirect('/d_admin')
    else:
          messages.error(request, "error.")
    return render(request,"action/d_admin.html")

def p_admin(request):
    patient=pmodels.Patient.objects.all()
    return render(request,"action/p_admin.html",{'patient':patient})

def d_admin(request):
    donor=dmodels.Donor.objects.all()
    return render(request,"action/d_admin.html",{'donor':donor})


def bloodstock(request):
    A1 = Stock.objects.get(bloodgroup="A+")
    B1 = Stock.objects.get(bloodgroup="B+")
    A2 = Stock.objects.get(bloodgroup="A-")
    B2 = Stock.objects.get(bloodgroup="B-")
    AB1 = Stock.objects.get(bloodgroup="AB+")
    AB2 = Stock.objects.get(bloodgroup="AB-")
    O1 = Stock.objects.get(bloodgroup="O+")
    O2 = Stock.objects.get(bloodgroup="O-")
    if request.method=="POST":
        bloodgroup=request.POST['bloodgroup']
        unit=request.POST['unit']
        stock=Stock.objects.get(bloodgroup=bloodgroup)
        stock.unit=unit
        stock.save()
        return redirect('/bloodstock')
    return render(request,"action/bloodstock.html",{'A1':A1,'B1':B1,'A2':A2,'B2':B2,'AB1':AB1,'AB2':AB2,'O1':O1,'O2':O2})

def donations(request):
    donation=dmodels.BloodDonate1.objects.all()
    return render(request,"action/donation.html",{'donation':donation})


def blood_request(request):
    
    blood_request=BloodRequest.objects.all()
    return render(request,"action/bloodrequest.html",{'blood_request':blood_request})


def approvep(request,id):
    patient=BloodRequest.objects.get(pk=id)
    bloodgroup=patient.bloodgroup
    unit=patient.unit
    stock=Stock.objects.get(bloodgroup=bloodgroup)
    if stock.unit > unit:
        stock.unit=stock.unit-unit
        patient.status='Approved'
        patient.save()
        stock.save()
        
    else:
        messages.error(request, "Stock Doest Not Have Enough Blood To Approve This Request, Only "+str(stock.unit)+" Unit Available")
    return redirect('/blood_request')
    return render(request,"action/blood_request")

def approved(request,id):
        d=dmodels.BloodDonate1.objects.get(pk=id)
        bloodgroup=d.bloodgroup
        unit=d.unit
        stock=Stock.objects.get(bloodgroup=bloodgroup)
        stock.unit=stock.unit+unit
        stock.save()

        d.status='Approved'
        d.save()
        messages.success(request, "Stock has been addedd")
        return redirect('/donations')
        return render(request,"action/donations.html")

def rejectp(request,id):
    patient1=BloodRequest.objects.get(pk=id)
    patient1.status='Rejected'
    patient1.save()
    messages.success(request, "Request has been rejected")
    return redirect('/blood_request')
    return render(request,"action/blood_request.html")

def rejectd(request,id):
    patient1=dmodels.BloodDonate1.objects.get(pk=id)
    patient1.status='Rejected'
    patient1.save()
    messages.success(request, "Request has been rejected")
    return redirect('/donations')
    return render(request,"action/dbloodrequest.html")

