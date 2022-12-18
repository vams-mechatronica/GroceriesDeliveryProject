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

User = get_user_model()

def index(request):
    if request.user.id != None:
        user_details = User.objects.get(pk = request.user.id)
    else:
        user_details = "Please select user"
    banners = Banners.objects.all()
    products = CategoriesProducts.objects.all()
    context = ({'products':products,'user':user_details,'banners':banners})
    return render(request,"index.html",context=context)


# Create your views here.
class ProductDetails(APIView):
    permission_classes = (AllowAny,)
    def get(self, req, format=None):
        tbl_product = Products.objects.all()
        serializer = ProductsSerializer(instance=tbl_product, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


def seeAllProductsInCategory(request,pk):
    categorydetails = Categories.objects.get(pk = pk)
    productdetail = CategoriesProducts.objects.filter(category = categorydetails.category_id)
    print(categorydetails)
    context = {'category':categorydetails,
                'products':productdetail,
            }
    return render(request,"list.html",context)

def productDetailsPageView(request,pk):
    productdetail = Products.objects.get(pk=pk)
    context = {
        'product':productdetail
    }
    return render(request,"detail-page.html",context)

def cartCheckoutPageView(request):
    return render(request,"cart.html")