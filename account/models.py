from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(null=True,blank=True,max_length=100)
    last_name = models.CharField(null=True,blank=True,max_length=100)
    email = models.EmailField(null=True)
    mobileno = models.CharField(null=False,max_length=10,default="",unique=True)
    username = models.CharField(null=True,max_length=50,unique=True)
    address = models.CharField(null=True,max_length=255,default="")

    USERNAME_FIELD: str = 'mobileno'
    REQUIRED_FIELDS: str = ('email',)

    objects = CustomUserManager()


    def __str__(self) -> str:
        return self.mobileno