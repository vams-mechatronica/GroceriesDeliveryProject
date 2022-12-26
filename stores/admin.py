from django.contrib import admin
from .models import *
# Register your models here.
class StoreProductsAdmin(admin.ModelAdmin):
    list_display: list = ('store','category','products','available_stock')
    ordering: list = ['-available_stock']
    search_fields: list = ('store','products','available_stock')

admin.site.register(StoreProductsDetails,StoreProductsAdmin)

class StoreDetailsAdmin(admin.ModelAdmin):
    list_display: list = ('storeName','storeAddress','storeLocalityPinCode')
    ordering: list = ['-storeLocalityPinCode']
    search_fields: list = ('storeName','storeLocalityPinCode','storeServicablePinCodes')

admin.site.register(StoreDetail,StoreDetailsAdmin)