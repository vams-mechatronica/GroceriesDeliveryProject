from django.db import models
from products.models import * 
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# Create your models here.

class StoreDetail(models.Model):
    storeName = models.CharField(_("Store Name"), max_length=50,null=False,default="")
    storeAddress = models.CharField(_("Store Address"), max_length=250,null=False,default="")
    storeLocality = models.CharField(_("Store Locality"), max_length=50,null=False,default= "")
    storeLocalityPinCode = models.IntegerField(_("Store Locality Pincode"))
    storeServicablePinCodes = models.CharField(_("Store Servicable Pincodes"), max_length=2048,default="")

    def __str__(self) -> str:
        return "Store Name: {} Store PinCode: {}".format(self.storeName,self.storeLocalityPinCode)

class StoreProductsDetails(models.Model):
    store = models.ForeignKey("stores.StoreDetail", verbose_name=_("Store Detail"), on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, verbose_name=_("store product categories"), on_delete=models.CASCADE)
    products = models.ForeignKey(Products, verbose_name=_("store products"), on_delete=models.CASCADE)
    discount = models.DecimalField(_("Discount"), max_digits=5, decimal_places=2,null=True,blank=True)
    list_price = models.DecimalField(_("Our Price"), max_digits=8, decimal_places=2,null=True)
    net_content = models.CharField(max_length=50,default="",null=True)
    item_package_quantity = models.CharField(max_length=50,default="",null=True)
    expiry_date = models.DateField(_("Expiry Date"), auto_now=False, auto_now_add=False,blank=True,null=True)
    packing_date = models.DateField(_("Packing Date"), auto_now=False, auto_now_add=False,null=True)
    available_stock = models.IntegerField(_("available stock"),default=0)

    def __str__(self) -> str:
        return "StoreName: {} ProductName: {} AvailableStock: {}".format(self.store,self.products,self.available_stock)
    
    