from django.contrib import admin
from .models import *

# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    list_display: list = ('product_name','brand','material_feature','unit','max_retail_price','created_at')
    ordering: list = ['-created_at']
    search_fields: list = ('product_name','brand','material_feature','max_retail_price')

admin.site.register(Products,ProductsAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    list_display: list = ('category_id','category_name')
    search_fields: list = ('category_id','category_name')

admin.site.register(Categories,CategoriesAdmin)

class ProductImagesAdmin(admin.ModelAdmin):
    list_display: list = ('images',)
    search_fields: list = ('images',)

admin.site.register(ProductImages,ProductImagesAdmin)

class ProductRARAdmin(admin.ModelAdmin):
    list_display: list = ('author','ratings','review')
    search_fields: list = ('author','ratings')

admin.site.register(ProductReviewAndRatings,ProductRARAdmin)

class BannersAdmin(admin.ModelAdmin):
    list_display: list = ('banner_name','banner_status','banner_images')
    search_fields: list = ('banner_status','banner_name')

admin.site.register(Banners,BannersAdmin)

# class CategoriesProductsAdmin(admin.ModelAdmin):
#     list_display: list = ('categoriesproduct_id',)
#     search_fields: list = ('categoriesproduct_id',)

admin.site.register(CategoriesProducts)