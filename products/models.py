from django.db import models
from django.utils.translation import gettext_lazy as _
from .storage import ProductFileStorage
from django.contrib.auth import get_user_model
from datetime import date

user = get_user_model()

# Create your models here.
class ProductReviewAndRatings(models.Model):
    RATINGS = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),)
    author = models.ForeignKey(user, verbose_name=_("Author Id"), on_delete=models.CASCADE)
    review = models.CharField(_("Product Review"), max_length=1024,null=True)
    ratings = models.CharField(_("Product Rating"), max_length=50,choices=RATINGS,null=True)
    upload_image = models.ImageField(_("ImagesForReview"),upload_to=ProductFileStorage(name='review',id=date.today().strftime("%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None,null=True)

    def __str__(self):
        return "Author ID: {}, Ratings: {}".format(self.author,self.ratings)

class Products(models.Model):
    FEATURE = (('NON VEG','NON VEGETERIAN'),('VEG','VEGETERIAN'),)

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=150)
    display_name = models.CharField(max_length=150)
    short_desc = models.TextField(max_length=250,null=True,blank=True)
    long_desc = models.TextField(max_length=1024,null=True,blank=True)
    max_retail_price = models.DecimalField(_("MRP"), max_digits=8, decimal_places=2)
    discount = models.CharField(_("Discount"), max_length=8)
    list_price = models.DecimalField(_("Our Price"), max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=50)
    material_feature = models.CharField(max_length=50, blank=True, choices=FEATURE)
    brand = models.CharField(max_length=250,default="",null=True)
    flavour = models.CharField(max_length=250,default="",null=True)
    net_content = models.CharField(max_length=50,default="",null=True)
    item_package_quantity = models.CharField(max_length=50,default="",null=True)
    expiry_date = models.DateField(_("Expiry Date"), auto_now=False, auto_now_add=False)
    packing_date = models.DateField(_("Packing Date"), auto_now=False, auto_now_add=False)
    prodimages = models.ImageField(_("Product Images"),upload_to=ProductFileStorage(name='product',id=date.today().strftime("%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None,null=True,default=None,blank=True)
    prodreviews = models.ForeignKey(ProductReviewAndRatings, verbose_name=_("ProdReviews"),related_name="prodReviews", on_delete=models.CASCADE,null=True)

    
    def __str__(self):
        return "Product Name: {}".format(self.product_name)

    def get_attrib_id(self):
        return self.product_id
    
    class Meta:
        db_table = "Product"
class ProductImages(models.Model):
    image_id = models.AutoField(_("Image Id"),primary_key=True)
    images = models.ImageField(_("Product Image"),upload_to=ProductFileStorage(name='product',id=date.today().strftime("%Y%m%d")).uploadImage, height_field=None, width_field=None, max_length=None)
    products = models.ForeignKey(Products,on_delete=models.CASCADE)

    def __str__(self):
        return "Image URL: {}".format(self.images)

class Categories(models.Model):               #----Catagory Details----#
    CATEGORIES = (('Bread & Milk','BREAD & MILK'),('Vegetables','VEGETABLES'),('Breakfast & Dairy','BREAKFAST & DAIRY'),('Biscuits, Snacks & Chocolates','BISCUITS, SNACKS & CHOCOLATES'),('Medicines','MEDICINES'),('Pan Corner','PAN CORNER'),('Comida','COMIDA'),('Trending','TRENDING'),)
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255,choices=CATEGORIES,null= False,default=None)
    short_desc = models.TextField(null = True, default = None,blank=True,max_length=1024)
    long_desc = models.TextField(null = True, default = None,blank=True,max_length=1024)
    products = models.ForeignKey(Products,on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return "Categories ID: {}, Product ID: {}".format(self.category_id,self.products)
    
    class Meta:
        db_table = "Categories"







