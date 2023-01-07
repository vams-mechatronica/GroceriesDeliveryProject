from django.contrib import admin
from .models import *

# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    list_display: list = ('product_name','unit','prod_mainimage','max_retail_price','modified_at')
    ordering: list = ['-modified_at']
    search_fields: list = ('product_name','material_feature','max_retail_price','pro_category')

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
    list_display: list = ('banner_name','banner_status','banner_images','position')
    search_fields: list = ('banner_status','banner_name')

admin.site.register(Banners,BannersAdmin)

# class CategoriesProductsAdmin(admin.ModelAdmin):
#     list_display: list = ('categoriesproduct_id',)
#     search_fields: list = ('categoriesproduct_id',)

admin.site.register(CategoriesProducts)