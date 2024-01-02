from django.db import models
from patient import models as pmodels
from donor import models as dmodels
from django.contrib.auth.models import User

class Donor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobileno = models.CharField(max_length=20,null=False)
    address = models.CharField(max_length=40)
    bloodgroup=models.CharField(max_length=10)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

class BloodDonate1(models.Model): 
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE)   
    firstname=models.CharField(max_length=40)
    lastname=models.CharField(max_length=40)
    mobileno=models.IntegerField(max_length=10)
    address=models.CharField(max_length=100)
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=20,default="Pending")
    def __str__(self):
        return self.donor