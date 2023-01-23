from django.db import models
from django.utils.translation import gettext_lazy as _
from .storage import ProductFileStorage
from django.contrib.auth import get_user_model
from datetime import date
from django import forms
from django.contrib.postgres.fields import ArrayField
from django_quill.fields import QuillField

user = get_user_model()
#MultiArrayChoiceFields

class ModifiedArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
            "widget": forms.CheckboxSelectMultiple,
            **kwargs
        }
        return super(ArrayField, self).formfield(**defaults)

# Create your models here.
class Products(models.Model):
    CATEGORIES = (('Tea & Coffee','Tea & Coffee'),('Fruits & Vegetables','Fruits & Vegetables'),('Breakfast & Dairy','BREAKFAST & DAIRY'),('Snacks & Drinks','Snacks & Drinks'),('Puja Store','Puja Store'),('Dry Fruits','Dry Fruits'),('Trending','TRENDING'),('Home & Kitchen Appliances','Home & Kitchen Appliances'),('Cleaning Essentials','Cleaning Essentials'),('Personal Care','Personal Care'),('Cooking Essentials','Cooking Essentials'),('Health & Baby Care','Health & Baby Care'))

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=150)
    desc = QuillField(null=True,blank=True)
    unit = models.CharField(max_length=50,blank=True)
    pro_category = ModifiedArrayField(models.CharField(_("Product Category"),max_length=255,choices=CATEGORIES,null = True,blank=True),null=True)
    max_retail_price = models.DecimalField(_("MRP (in Rs.)"), max_digits=8, decimal_places=2,null=True)
    prod_mainimage = models.ImageField(_("Product Main Image"),upload_to=ProductFileStorage(name='product',id=date.today().strftime("%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None,null=True,default=None,blank=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True)
    
    def __str__(self):
        return "Name: {} \tUnit: {}\t MRP: {}".format(self.product_name,self.unit,self.max_retail_price)

    def get_attrib_id(self):
        return self.product_id
    
    class Meta:
        db_table = "Product"
        verbose_name_plural = 'Products'

class ProductReviewAndRatings(models.Model):
    RATINGS = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),)
    author = models.ForeignKey(user, verbose_name=_("Author Id"), on_delete=models.CASCADE)
    review = models.CharField(_("Product Review"), max_length=1024,null=True)
    ratings = models.CharField(_("Product Rating"), max_length=50,choices=RATINGS,null=True)
    upload_image = models.ImageField(_("ImagesForReview"),upload_to=ProductFileStorage(name='review',id=date.today().strftime("%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None,null=True)
    review_date = models.DateTimeField(verbose_name="review_date",auto_now=True)
    prodreviews = models.ForeignKey(Products, verbose_name=_("ProdReviews"),related_name="prodReviews", on_delete=models.CASCADE,null=True)

    def __str__(self):
        return "Author ID: {}, Ratings: {}".format(self.author,self.ratings)

class ProductImages(models.Model):
    image_id = models.AutoField(_("Image Id"),primary_key=True)
    images = models.ImageField(_("Product_Image"),upload_to=ProductFileStorage(name='product',id=date.today().strftime("%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None)
    products = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="prodImages")

    def __str__(self):
        return "Image URL: {}".format(self.images)

class Categories(models.Model):               #----Catagory Details----#
    
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255,null= False,default=None,unique=True)
    desc = models.TextField(null = True, default = None,blank=True,max_length=1024)
    category_image = models.ImageField(_("category image"), upload_to=ProductFileStorage(name='category',id=date.today().strftime("%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None,null=True,blank=True)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        db_table = "Categories"
        verbose_name_plural = 'Categories'

class CategoriesProducts(models.Model):
    categoriesproduct_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, verbose_name=_("Pro Category"), on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name=_("Category Products"), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "ID: {} Category: {} Products: {}".format(self.categoriesproduct_id,self.category,self.product)
    
    class Meta:
        db_table = "CategoriesProducts"
        verbose_name_plural = 'CategoriesProducts'

class Banners(models.Model):
    ChoiceStatus = (('Activate','ACTIVATE'),('Deactivate','DEACTIVATE'),)
    BannerPosition = (("Home","HOME"),('Categories','CATEGORIES'),('Top','TOP'),('Middle','MIDDLE'),('Bottom','BOTTOM'),)
    position = ModifiedArrayField(models.CharField(_("Banner Position"),max_length=255,choices=BannerPosition,null = True,blank=True),blank=True,null=True)
    banner_name = models.CharField(_("bannername"), max_length=50,null=True,blank=True)
    banner_images = models.ImageField(_("bannerimages"), upload_to=ProductFileStorage(name='banners',id=date.today().strftime("%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None)
    banner_status = models.CharField(max_length=20,choices=ChoiceStatus,null=False,default=None)

    def __str__(self):
        return "Banner Name: {}, Banner Status: {}".format(self.banner_name,self.banner_status)
    
    class Meta:
        db_table = "Banners"
        verbose_name_plural = 'Banners'








