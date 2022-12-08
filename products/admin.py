from django.contrib import admin
from .models import *

# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    list_display: list = ('product_name','max_retail_price','discount','brand','list_price')
    ordering: list = ['-expiry_date']
    search_fields: list = ('product_name','discount','brand','expiry_date')

admin.site.register(Products,ProductsAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    list_display: list = ('category_name','products')
    search_fields: list = ('category_name','products__product_name')

admin.site.register(Categories,CategoriesAdmin)

class ProductImagesAdmin(admin.ModelAdmin):
    list_display: list = ('images',)
    search_fields: list = ('images',)

admin.site.register(ProductImages,ProductImagesAdmin)

class ProductRARAdmin(admin.ModelAdmin):
    list_display: list = ('author','ratings','review')
    search_fields: list = ('author','ratings')

admin.site.register(ProductReviewAndRatings,ProductRARAdmin)
