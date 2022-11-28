from django.contrib import admin
from .models import *

# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    list_display: list = ('product_name','max_retail_price','discount','brand')
    ordering: list = ['-expiry_date']
    search_fields: list = ('product_name','discount','brand','expiry_date')

admin.site.register(Products,ProductsAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    list_display: list = ('category_name','product_id')
    search_fields: list = ('category_name','product_id')

admin.site.register(Categories,CategoriesAdmin)

class ProductImagesAdmin(admin.ModelAdmin):
    list_display: list = ('product_id','images')
    search_fields: list = ('product_id',)

admin.site.register(ProductImages,ProductImagesAdmin)

class ProductRARAdmin(admin.ModelAdmin):
    list_display: list = ('author_id','product_id','rating','review')
    search_fields: list = ('author_id','product_id','rating')

admin.site.register(ProductReviewAndRatings,ProductRARAdmin)
