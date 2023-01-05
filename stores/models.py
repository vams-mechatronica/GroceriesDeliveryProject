from django.db import models
from products.models import * 
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# Create your models here.
RATINGS = ((1,1),(2,2),(3,3),(4,4),(5,5),)

class StoreDetail(models.Model):
    storeName = models.CharField(_("Store Name"), max_length=50,null=False,default="")
    storeAddress = models.CharField(_("Store Address"), max_length=250,null=False,default="",blank=False)
    storeLocality = models.CharField(_("Store Locality"), max_length=50,null=False,default= "",blank=False)
    storeLocalityPinCode = models.IntegerField(_("Store Locality Pincode"),null=True,blank=True)
    storeServicablePinCodes = models.CharField(_("Store Servicable Pincodes"), max_length=2048,default="",null=True,blank=True)
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
    discount = models.DecimalField(_("Discount"), max_digits=5, decimal_places=2,null=True,blank=True)
    list_price = models.DecimalField(_("Our Price"), max_digits=8, decimal_places=2,null=True)
    available_stock = models.IntegerField(_("available stock"),default=0)
    status = models.BooleanField(_("Product Status"),default=True)
    
    def __str__(self) -> str:
        return "StoreName: {} ProductName: {} AvailableStock: {}".format(self.store,self.products,self.available_stock)
    
    