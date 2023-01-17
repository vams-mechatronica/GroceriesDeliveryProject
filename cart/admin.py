from django.contrib import admin
from .models import *

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display: list = ('user','itemname','storename','itemavailablestock','quantity','ordered')
    ordering: list = ['user']
    search_fields: list = ('user','ordered')

    def storename(self,obj):
        return obj.item.store.storeName

    def itemname(self,obj):
        return obj.item.products.product_name

    def itemavailablestock(self,obj):
        return obj.item.available_stock

admin.site.register(Cart,CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display: list = ('user','ref_code','items_get','ordered','ordered_date','shipping_address','payment','received','refund_requested')
    ordering: list = ['user','ref_code','ordered','ordered_date','payment','refund_requested']
    search_fields: list = ('user','red_code','ordered','ordered_date','payment','refund_requested','shipping_address')

    def items_get (self,obj):
        return [item.item.products.product_name for item in obj.items.all()]
admin.site.register(Order,OrderAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display: list =('instamojo_id','user','amount','timestamp')

admin.site.register(Payment,PaymentAdmin)
