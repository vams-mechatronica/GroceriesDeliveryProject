from django.contrib import admin
from .models import *
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display: list = ('username','first_name','mobileno','email','date_joined')
    ordering: list = ['-date_joined']
    search_fields: list = ('email','mobileno','first_name','last_name','username')

admin.site.register(CustomUser,CustomUserAdmin)

admin.site.register(UserAddresses)
admin.site.register(Country)
admin.site.register(DeviceOtp)
