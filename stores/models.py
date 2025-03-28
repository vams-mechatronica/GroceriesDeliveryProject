from django.db import models
from products.models import * 
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.contrib.postgres.fields import ArrayField

# Create your models here.
RATINGS = ((1,1),(2,2),(3,3),(4,4),(5,5),)

class StoreDetail(models.Model):
    storeName = models.CharField(_("Store Name"), max_length=50,null=False,default="")
    storeAddress = models.CharField(_("Store Address"), max_length=250,null=False,default="",blank=False)
    storeLocality = models.CharField(_("Store Locality"), max_length=50,null=False,default= "",blank=False)
    storeLocalityPinCode = models.IntegerField(_("Store Locality Pincode"),null=True,blank=True)
    storeServicablePinCodes = ArrayField(models.CharField(_("Store Servicable Pincodes"), max_length=2048,default="",null=True,blank=True),null=True,blank=True)
    storePhoneNo = models.CharField(_("Store Phone No."),max_length=15,null=True,blank=True)
    storeEmail = models.EmailField(_("Store Email ID"), max_length=254,null= True,blank=True)
    storeRating = models.IntegerField(_("Store Rating"),choices=RATINGS,null=True,blank=True)
    storeStatus = models.BooleanField(_("Store Status"),default=True)

    def __str__(self) -> str:
        return self.storeName
    
    def fullStoreAddress(self):
        addr = self.storeAddress + ", " +self.storeLocality +", " + str(self.storeLocalityPinCode)
        return addr

class StoreProductsDetails(models.Model):
    store = models.ForeignKey("stores.StoreDetail", verbose_name=_("Store Detail"), on_delete=models.CASCADE)
    products = models.ForeignKey(Products, verbose_name=_("store products"), on_delete=models.CASCADE)
    discount = models.DecimalField(_("Discount (in Rs.)"), max_digits=5, decimal_places=2,null=True,blank=True)
    available_stock = models.IntegerField(_("available stock (in Nos.)"),default=0)
    display_home = models.BooleanField(_("Display at home"),default=False)
    status = models.BooleanField(_("Product Status"),default=True)
    
    def __str__(self) -> str:
        return "StoreName: {} ProductName: {} AvailableStock: {}".format(self.store,self.products,self.available_stock)
    
    def list_price(self):
        listprice = self.products.max_retail_price - self.discount
        return round(listprice,2)
    
class storeServiceLocation(models.Model):
    store = models.ForeignKey("StoreDetail", verbose_name=_("Store Delivery Location"), on_delete=models.CASCADE)
    area = models.CharField(
        _("Delivery Area"), max_length=500, null=True, default="", blank=True)
    sector = models.CharField(
        _("Delivery Sector"), max_length=500, null=True, default="", blank=True)
    city = models.CharField(
        _("Delivery City"), max_length=500, null=True, default="", blank=True)
    pincode = models.IntegerField(_("Delivery Pincode"))

    def __str__(self) -> str:
        return "StoreName: {}\t Sector: {}\t Area: {}\t Pincode: {}".format(self.store,self.sector,self.area,self.pincode)
    
    def comb_area(self):
        return "{}, {}, {}".format(self.area,self.sector,self.city)

class ContactUs(models.Model):
    name = models.CharField(
        _("Customer Name"), max_length=100, null=True, default="", blank=True)
    email = models.EmailField(
        _("Customer Email"), max_length=254, null=True, default="", blank=True)
    phone = models.CharField(_("Customer Phone No."),
                             max_length=100, null=True, default="", blank=True)
    subject = models.CharField(
        _("Subject"), max_length=100, null=True, default="", blank=True)
    message = models.CharField(
        _("Message"), max_length=2000, null=True, default="", blank=True)

    created_at = models.DateTimeField(
        _("Message Created At"), auto_now=True)

    def __str__(self) -> str:
        return self.name

