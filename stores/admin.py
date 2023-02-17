from django.contrib import admin
from .models import *
# Register your models here.
class StoreProductsAdmin(admin.ModelAdmin):
    list_display: list = ('pname','unit','mrp','discount','ourprice','display_home','available_stock','storename')
    ordering: list = ['-available_stock']
    search_fields: list = ('storeAddress','products','available_stock')

    def storeAddress(self,obj):
        return obj.store.fullStoreAddress()
    
    def mrp(self,obj):
        return obj.products.max_retail_price
    
    def unit(self,obj):
        return obj.products.unit
    
    def pname(self,obj):
        return obj.products.product_name
    
    def ourprice(self,obj):
        list_price = obj.products.max_retail_price - ((obj.discount/100) * obj.products.max_retail_price)
        return round(list_price,2)

    def storename(self,obj):
        return obj.store.storeName
admin.site.register(StoreProductsDetails,StoreProductsAdmin)

class StoreDetailsAdmin(admin.ModelAdmin):
    list_display: list = ('storeName','fullStoreAddress','storeEmail','storePhoneNo','storeRating','storeStatus','storeServicablePinCodes',)
    ordering: list = ['-storeLocalityPinCode']
    search_fields: list = ('storeName','storeLocalityPinCode','storeServicablePinCodes','storeRating','storeStatus')

admin.site.register(StoreDetail,StoreDetailsAdmin)

class StoreDeliveryLocationAdmin(admin.ModelAdmin):
    list_display: list = ('store', 'area', 'sector','pincode')
    ordering: list = ['pincode','sector']
    search_fields: list = ('store', 'area', 'sector', 'pincode')

admin.site.register(storeServiceLocation,StoreDeliveryLocationAdmin)
