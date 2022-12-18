from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager
from products.storage import ProductFileStorage
from datetime import date
from django.utils.translation import gettext_lazy as _



# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(null=True,blank=True,max_length=100)
    last_name = models.CharField(null=True,blank=True,max_length=100)
    email = models.EmailField(null=True)
    mobileno = models.CharField(verbose_name="Mobile Number",null=False,max_length=10,default="",unique=True)
    username = models.CharField(null=True,max_length=50,unique=True)
    address = models.CharField(null=True,max_length=255,default="")
    avatar = models.ImageField(_("Avatar"),upload_to=ProductFileStorage(name='user',id=date.today().strftime("%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None,null=True,blank=True)

    USERNAME_FIELD: str = 'mobileno'
    REQUIRED_FIELDS: str = ('email',)

    objects = CustomUserManager()


    def __str__(self) -> str:
        return self.mobileno