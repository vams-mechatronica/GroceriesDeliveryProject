from django.contrib import admin
from .models import *
# Register your models here.
class StoreProductsAdmin(admin.ModelAdmin):
    list_display: list = ('products','category','net_content','mrp','discount','list_price','trending','store','storeAddress','expiry_date','packing_date','available_stock','item_package_quantity')
    ordering: list = ['-available_stock','expiry_date']
    search_fields: list = ('store','products','available_stock','expiry_date','packing_date','trending')

    def storeAddress(self,obj):
        return obj.store.fullStoreAddress()
    
    def mrp(self,obj):
        return obj.products.max_retail_price

admin.site.register(StoreProductsDetails,StoreProductsAdmin)

class StoreDetailsAdmin(admin.ModelAdmin):
    list_display: list = ('storeName','fullStoreAddress','storeEmail','storePhoneNo','storeRating','storeStatus','storeServicablePinCodes',)
    ordering: list = ['-storeLocalityPinCode']
    search_fields: list = ('storeName','storeLocalityPinCode','storeServicablePinCodes','storeRating','storeStatus')

admin.site.register(StoreDetail,StoreDetailsAdmin)