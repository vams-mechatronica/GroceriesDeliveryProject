from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager
from products.storage import ProductFileStorage
from datetime import date
from django.utils.translation import gettext_lazy as _
import uuid

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
    user = models.OneToOneField("user.CustomUser", verbose_name=_(
        "User Detail"), on_delete=models.CASCADE, null=True, blank=True)
    addressLine1 = models.CharField(
        _("address line 1"), max_length=200, blank=True, null=True)
    addressLine2 = models.CharField(
        _("address line 2"), max_length=150, blank=True, null=True)
    state = models.CharField(
        _("select state"), max_length=200, blank=True, null=True)
    city = models.CharField(
        _("select city"), max_length=200, blank=True, null=True)
    pincode = models.IntegerField(_("address pincode"))
    addPhoneNumber = models.CharField(
        _("address phone number"), max_length=13, null=True, blank=True)

    def __str__(self) -> str:
        return "user:{} city: {} pincode: {} phoneno. {}".format(self.user, self.city, self.pincode, self.addPhoneNumber)

    def user_address(self):
        address = self.addressLine1+", "+self.addressLine2 + \
            ", "+self.city+", " + str(self.pincode)
        return address


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
