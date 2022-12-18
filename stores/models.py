from django.db import models
from products.models import * 
from django.utils.translation import gettext_lazy as _

# Create your models here.

class store(models.Model):
    store_name = models.CharField(_("store name"), max_length=50,null=False)
    store_address = models.CharField(_("store address"), max_length=500,null=False)
    category = models.ForeignKey(Categories, verbose_name=_("store product categories"), on_delete=models.CASCADE)
    products = models.ForeignKey(Products, verbose_name=_("store products"), on_delete=models.CASCADE)
    available_stock = models.IntegerField(_("available stock"))

    def __str__(self) -> str:
        return "StoreName: {} ProductName: {} AvailableStock: {}".format(self.store_name,self.products,self.available_stock)
    
    