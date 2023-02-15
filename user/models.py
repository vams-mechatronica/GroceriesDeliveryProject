from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager
from products.storage import ProductFileStorage
from datetime import date
from django.utils.translation import gettext_lazy as _
import uuid
from django.db.models import Q
# Create your models here.


class CustomUser(AbstractUser):
    first_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    email = models.EmailField(null=True)
    mobileno = models.CharField(verbose_name="Mobile Number",
                              null=False, max_length=10, default="", unique=True)
    username = models.CharField(null=True, max_length=50, unique=True)
    avatar = models.ImageField(_("Avatar"), upload_to=ProductFileStorage(name='user', id=date.today().strftime(
        "%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None, null=True, blank=True)

    USERNAME_FIELD: str = 'mobileno'
    REQUIRED_FIELDS: str = ('email',)

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.mobileno

    def user_full_name(self):
        return self.first_name + " " + self.last_name


class UserAddresses(models.Model):
    ADDRESS = (('Home','Home'),('Office','Office'),('Others','Others'))
    user = models.ForeignKey("user.CustomUser", verbose_name=_(
        "User Detail"), on_delete=models.CASCADE, null=True, blank=True)
    default_address = models.BooleanField(_("Default Address"),null=True,blank=True,default=True)
    contact_name = models.CharField(
        _("Contact Name"), max_length=50, default='', null=True, blank=True)
    address_name = models.CharField(_("Address Name"), max_length=50,choices=ADDRESS,default='Home',null=True,blank=True)
    addressLine1 = models.CharField(
        _("address line 1"), max_length=2000, blank=True, null=True,default=" ")
    state = models.CharField(
        _("select state"), max_length=200, blank=True, null=True,default=" ")
    city = models.CharField(
        _("select city"), max_length=200, blank=True, null=True,default=" ")
    pincode = models.IntegerField(_("address pincode"))
    mobileno = models.CharField(
        _("address phone number"), max_length=13, null=True, blank=True,default=" ")

    def __str__(self) -> str:
        return "user:{} city: {} pincode: {} phoneno. {}".format(self.user, self.city, self.pincode, self.mobileno)

    def user_address(self):
        address = str(self.addressLine1)+", "+str(self.city)+", " + str(self.pincode)
        return address
    
    def save(self, *args, **kwargs):
        if self.default_address:
            self.__class__._default_manager.filter(
                user=self.user, default_address=True ).update(default_address=False)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(default_address=True),
                name='unique_primary_per_customer'
            )
        ]


class Country(models.Model):
    country_code = models.CharField(max_length=4, blank=True, null=True)
    country_name = models.CharField(max_length=50, blank=True, null=True)
    nick_name = models.CharField(max_length=5, blank=True, null=True)
    country_image = models.CharField(max_length=200, blank=True, null=True)
    country_image_2 = models.ImageField(upload_to='country', null=True)
    is_top = models.BooleanField(_('is_top'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    created_date = models.DateTimeField(_('created date'), auto_now_add=True)

    def __str__(self):
        return self.country_name


class DeviceOtp(models.Model):
    country = models.ForeignKey(
        Country, related_name='device_country_user', on_delete=models.CASCADE, null=True)
    number = models.CharField(max_length=50, blank=False, null=False)
    otp = models.IntegerField(blank=True, null=True, default=0)
    session = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=False)
    auth_token = models.UUIDField(
        _("auth_token"), null=True, blank=True, default=uuid.uuid4)
    created_date = models.DateTimeField('date created', auto_now_add=True)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return self.number
