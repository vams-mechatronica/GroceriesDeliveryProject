from django.db import models
from django.utils.translation import gettext_lazy as _
from .storage import ProductFileStorage
from django.contrib.auth import get_user_model

user = get_user_model()

# Create your models here.
class Products(models.Model):
    FEATURE = (('NON VEG','NON VEGETERIAN'),('VEG','VEGETERIAN'),)

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=150)
    display_name = models.CharField(max_length=150)
    short_desc = models.TextField(max_length=250,null=True,blank=True)
    long_desc = models.TextField(max_length=1024,null=True,blank=True)
    max_retail_price = models.DecimalField(_("MRP"), max_digits=8, decimal_places=2)
    discount = models.DecimalField(_("Discount"), max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=50)
    material_feature = models.CharField(max_length=50, blank=True, choices=FEATURE)
    brand = models.CharField(max_length=250,default="",null=True)
    flavour = models.CharField(max_length=250,default="",null=True)
    net_content = models.CharField(max_length=50,default="",null=True)
    item_package_quantity = models.CharField(max_length=50,default="",null=True)
    expiry_date = models.DateField(_("Expiry Date"), auto_now=False, auto_now_add=False)
    packing_date = models.DateField(_("Packing Date"), auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return "Product Name: {}".format(self.product_name)

    def get_attrib_id(self):
        return self.product_id
    
    class Meta:
        db_table = "Product"

    
    
class Categories(models.Model):               #----Catagory Details----#
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    short_desc = models.TextField(null = True, default = None,blank=True,max_length=1024)
    long_desc = models.TextField(null = True, default = None,blank=True,max_length=1024)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return "Categories ID: {}, Product ID: {}".format(self.category_id,self.product_id)
    
    class Meta:
        db_table = "Categories"


class ProductImages(models.Model):
    image_id = models.AutoField(_("Image Id"),primary_key=True)
    product_id = models.ForeignKey(Products, verbose_name=_("Product Id"), on_delete=models.CASCADE)
    images = models.ImageField(_("Product Image"), storage=ProductFileStorage(name='product',id=image_id).imageFileStorage, height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return "Product ID: {}, Image URL: {}".format(self.product_id,self.images)

class ProductReviewAndRatings(models.Model):
    RATINGS = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),)
    author_id = models.ForeignKey(user, verbose_name=_("Author Id"), on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, verbose_name=_("Product Id"), on_delete=models.CASCADE)
    review = models.CharField(_("Product Review"), max_length=1024,null=True)
    rating = models.CharField(_("Product Rating"), max_length=50,choices=RATINGS,null=True)
    upload_images = models.ImageField(_(""), storage=ProductFileStorage(name='review',id=author_id).imageFileStorage, height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return "Author ID: {}, Product Id: {}, Ratings: {}".format(self.author_id,self.product_id,self.rating)



