from django.contrib import admin
from .models import *
# Register your models here.
class storeAdmin(admin.ModelAdmin):
    list_display: list = ('store_name','category','products','available_stock')
    ordering: list = ['-available_stock']
    search_fields: list = ('store_name','products','available_stock')

admin.site.register(store,storeAdmin)