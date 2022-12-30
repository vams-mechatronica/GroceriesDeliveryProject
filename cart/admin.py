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
