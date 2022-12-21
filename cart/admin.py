from django.contrib import admin
from .models import *

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display: list = ('user','item','quantity','ordered')
    ordering: list = ['user']
    search_fields: list = ('user','ordered')

admin.site.register(Cart,CartAdmin)
