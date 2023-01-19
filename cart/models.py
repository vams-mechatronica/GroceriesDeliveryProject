from django.db import models
from django.conf import settings
from stores.models import *
from django.utils.translation import gettext_lazy as _



# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(StoreProductsDetails, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        verbose_name_plural = 'Cart'

    def __str__(self):
        return f"{self.quantity} of {self.item.products.product_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.products.max_retail_price

    def get_total_discount_item_price(self):
        return self.quantity * ((self.item.discount/100)*self.item.products.max_retail_price)

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()
    
    def amount_after_applying_discount(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount:
            return self.amount_after_applying_discount()
        return self.get_total_item_price()
    
    def get_product_name(self):
        return self.item.products.product_name

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=200, blank=True, null=True)
    items = models.ManyToManyField(Cart)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.CharField(_("shipping_address"), max_length=250,blank=True,null=True)
    billing_address = models.CharField(_("billing_address"), max_length=250,blank=True,null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    
    def get_max_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total
    
    def get_order_name(self):
        name = ''
        for order_item in self.items.all():
            name = order_item.get_product_name()
        return name
    
    def get_total_items_in_order(self):
        return len(self.items.all()) - 1
    
    def get_quantity(self):
        qty = 0
        for order_item in self.items.all():
            qty += order_item.quantity

        return qty
    
    def get_total_discount(self):
        return self.get_max_total() - self.get_total()


    
class Payment(models.Model):
    instamojo_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
