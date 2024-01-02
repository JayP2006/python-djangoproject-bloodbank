from django.db import models
from django.contrib.auth.models import User
class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobileno = models.CharField(max_length=20,null=False)
    address = models.CharField(max_length=40)
    bloodgroup=models.CharField(max_length=10)
    

    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name
