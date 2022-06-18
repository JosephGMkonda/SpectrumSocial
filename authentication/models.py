from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager


# Create your models here.
class User(AbstractBaseUser):
    username=models.CharField(max_length=250)
    email=models.EmailField(max_length=100,unique=True)
    phonenumber=models.CharField(max_length=100,blank=True)
    password=models.CharField(max_length=100)

    objects =  UserManager()
    
    def __str__(self):
        return self.username
