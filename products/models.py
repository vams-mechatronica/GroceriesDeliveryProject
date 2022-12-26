from django.db import models
from django.utils.translation import gettext_lazy as _
from .storage import ProductFileStorage
from django.contrib.auth import get_user_model
from datetime import date

user = get_user_model()

# Create your models here.
class Products(models.Model):
    FEATURE = (('NON VEG','NON VEGETERIAN'),('VEG','VEGETERIAN'),)

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=150)
    display_name = models.CharField(max_length=150)
    long_desc = models.TextField(max_length=5000,null=True,blank=True)
    unit = models.CharField(max_length=50)
    material_feature = models.CharField(max_length=50, blank=True, choices=FEATURE)
    brand = models.CharField(max_length=250,default="",null=True)
    flavour = models.CharField(max_length=250,default="",null=True)
    prod_mainimage = models.ImageField(_("Product Main Image"),upload_to=ProductFileStorage(name='product',id=date.today().strftime("%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None,null=True,default=None,blank=True)
    
    def __str__(self):
        return "Product Name: {}".format(self.product_name)

    def get_attrib_id(self):
        return self.product_id
    
    class Meta:
        db_table = "Product"

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
    CATEGORIES = (('Bread & Milk','BREAD & MILK'),('Vegetables','VEGETABLES'),('Breakfast & Dairy','BREAKFAST & DAIRY'),('Biscuits, Snacks & Chocolates','BISCUITS, SNACKS & CHOCOLATES'),('Medicines','MEDICINES'),('Pan Corner','PAN CORNER'),('Comida','COMIDA'),('Trending','TRENDING'),)
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255,choices=CATEGORIES,null= False,default=None,unique=True)
    short_desc = models.TextField(null = True, default = None,blank=True,max_length=1024)
    long_desc = models.TextField(null = True, default = None,blank=True,max_length=1024)
    category_image = models.ImageField(_("category image"), upload_to=ProductFileStorage(name='category',id=date.today().strftime("%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None,null=True)
    
    def __str__(self):
        return "Categories ID: {}, category's Name: {}".format(self.category_id,self.category_name)
    
    class Meta:
        db_table = "Categories"

class CategoriesProducts(models.Model):
    categoriesproduct_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, verbose_name=_("Pro Category"), on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name=_("Category Products"), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "ID: {} Category: {} Products: {}".format(self.categoriesproduct_id,self.category,self.product)
    
    class Meta:
        db_table = "CategoriesProducts"

class Banners(models.Model):
    ChoiceStatus = (('Activate','ACTIVATE'),('Deactivate','DEACTIVATE'),)
    position = models.CharField(_("position"), max_length=50,null=False)
    banner_name = models.CharField(_("bannername"), max_length=50,null=False)
    banner_images = models.ImageField(_("bannerimages"), upload_to=ProductFileStorage(name='banners',id=date.today().strftime("%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None)
    banner_status = models.CharField(max_length=20,choices=ChoiceStatus,null=False,default=None)

    def __str__(self):
        return "Banner Name: {}, Banner Status: {}".format(self.banner_name,self.banner_status)








