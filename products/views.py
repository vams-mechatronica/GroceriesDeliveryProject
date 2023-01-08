from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.views.generic import *
from user.models import *
from stores.models import *
from cart.models import *

User = get_user_model()

def index(request):
    if request.user.id != None:
        user_details = UserAddresses.objects.get(user = request.user.id)
        products = StoreProductsDetails.objects.filter(store__storeServicablePinCodes__contains = user_details.pincode)

    else:
        user_details = "Please select user"
        products = StoreProductsDetails.objects.all()
    banners = Banners.objects.all()
    categories = Categories.objects.all()
    context = ({'user':user_details,'banners':banners,'products':products,'categories':categories})
    return render(request,"index.html",context=context)


# Create your views here.
class ProductDetails(APIView):
    permission_classes = (AllowAny,)
    def get(self, req, format=None):
        tbl_product = Products.objects.all()
        serializer = ProductsSerializer(instance=tbl_product, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


def seeAllProductsInCategory(request,pk):
    counter = 0
    a = 0
    categorydetails = Categories.objects.get(pk = pk)
    if request.user.id != None:
        user_details = UserAddresses.objects.get(user = request.user.id)
        productdetail = StoreProductsDetails.objects.filter(products__pro_category__contains = [categorydetails.category_name],store__storeServicablePinCodes__contains = user_details.pincode)
        cartitems = Cart.objects.filter(user = request.user.id)
    else:
        productdetail = StoreProductsDetails.objects.filter(products__pro_category__contains = [categorydetails.category_name])
    
    for i in cartitems:
        counter += i.quantity
        a += i.get_total_item_price()

    context = {'category':categorydetails,
                'catproducts':productdetail,
                'totalcartitem':len(cartitems),
                'totalamount':a,
                'totalquantity':counter,
            }
    return render(request,"list.html",context)

def trendingAllItems(request):
    if request.user.id != None:
        user_details = UserAddresses.objects.get(user = request.user.id)
        productdetail = StoreProductsDetails.objects.filter(store__storeLocalityPinCode = user_details.pincode,trending = True)
        cartitems = Cart.objects.filter(user = request.user.id)
    else:
        productdetail = StoreProductsDetails.objects.filter(trending = True)
    
    for i in cartitems:
        counter += i.quantity
        a += i.get_total_item_price()

    context = {
                'products':productdetail,
                'totalcartitem':len(cartitems),
                'totalamount':a,
                'totalquantity':counter,
            }
    return render(request,"list_trending.html",context)



def productDetailsPageView(request,pk):
    counter = 0
    a = 0
    if request.user.id != None:
        user_details = UserAddresses.objects.get(user = request.user.id)
        products = StoreProductsDetails.objects.filter(store__storeServicablePinCodes__contains = user_details.pincode).get(products=pk)
        cartitems = Cart.objects.filter(user = request.user.id)
    else:
        user_details = "Please select user"
        products = StoreProductsDetails.objects.filter(products=pk,store__storeLocalityPinCode = 201301).get(products=pk)
    # productdetail = Products.objects.get(pk=pk)
    for i in cartitems:
        counter += i.quantity
        a += i.get_total_item_price()

    context = {
        'product':products,
        'totalcartitem':len(cartitems),
        'totalamount':a,
        'totalquantity':counter,
    }
    return render(request,"detail-page.html",context)

