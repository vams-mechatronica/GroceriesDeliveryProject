from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth
from rest_framework import generics,status,authentication,permissions
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.views.generic import *
from user.models import *
from stores.models import *
from cart.models import *
from django.http import JsonResponse

User = get_user_model()

def index(request):
    try:
        if request.user.is_authenticated:
            user_details = UserAddresses.objects.get(user = request.user.id)
            products = StoreProductsDetails.objects.filter(store__storeServicablePinCodes__contains = [user_details.pincode])

        else:
            user_details = "Please select user"
            products = StoreProductsDetails.objects.filter(
                store__storeServicablePinCodes__contains=[201301])
        banners = Banners.objects.all()
        categories = Categories.objects.all()
        context = ({'user':user_details,'banners':banners,'products':products,'categories':categories})
        return render(request,"index.html",context=context)
    except UserAddresses.DoesNotExist:
        user_details = request.user
        products = StoreProductsDetails.objects.filter(
            store__storeServicablePinCodes__contains=[201301])
        banners = Banners.objects.all()
        categories = Categories.objects.all()
        context = ({'user': user_details, 'banners': banners,
                    'products': products, 'categories': categories})
        return render(request, "index.html", context=context)



# Create your views here.
class ProductDetails(APIView):
    permission_classes = (AllowAny,)
    def get(self, req, format=None):
        tbl_product = Products.objects.all()
        serializer = ProductsSerializer(instance=tbl_product, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


def seeAllProductsInCategory(request,pk):
    categorydetails = Categories.objects.get(pk = pk)
    try:
        if request.user.id != None:
            user_details = UserAddresses.objects.get(user = request.user.id)
            productdetail = StoreProductsDetails.objects.filter(products__pro_category__contains = [categorydetails.category_name],store__storeServicablePinCodes__contains = [user_details.pincode])
            cartitems = Order.objects.get(user = request.user.id,ordered = False)
            if cartitems == None:
                context = {'category':categorydetails,
                        'catproducts':productdetail,
                        'totalcartitem':0,
                        'totalamount':0,
                        'totalquantity':0,
                    }
            else:
                context = {'category': categorydetails,
                        'catproducts': productdetail,
                        'totalcartitem': cartitems.get_total_items_in_order() + 1,
                        'totalamount': round(cartitems.get_total(), 2),
                        'totalquantity': cartitems.get_quantity(),
                        }
        else:
            productdetail = StoreProductsDetails.objects.filter(products__pro_category__contains = [categorydetails.category_name])
            
            context = {'category':categorydetails,
                        'catproducts':productdetail,
                        'totalcartitem':0,
                        'totalamount':0,
                        'totalquantity':0,
                    }
    except Order.DoesNotExist:
        context = {
            'category': categorydetails,
            'catproducts': productdetail,
            'totalcartitem': 0,
            'totalamount': 0,
            'totalquantity': 0,
        }

    return render(request,"list.html",context)

def productDetailsPageView(request,pk):
    counter = 0
    a = 0
    try:
        if request.user.id != None:
            user_details = UserAddresses.objects.get(user = request.user.id)
            products = StoreProductsDetails.objects.filter(store__storeServicablePinCodes__contains = [user_details.pincode]).get(products=pk)
            cartitems = Order.objects.get(user = request.user.id,ordered = False)
            context = {
                'product':products,
                'totalcartitem': cartitems.get_total_items_in_order() + 1,
                'totalamount': round(cartitems.get_total(), 2),
                'totalquantity': cartitems.get_quantity(),
            }
        else:
            user_details = "Please select user"
            products = StoreProductsDetails.objects.filter(
                products=pk, store__storeServicablePinCodes__contains=[201301]).get(products=pk)
        # productdetail = Products.objects.get(pk=pk)
            context = {
                'product':products,
                'totalcartitem':0,
                'totalamount':a,
                'totalquantity':counter,
            }
    
    except (Order.DoesNotExist,UserAddresses.DoesNotExist):
        products = StoreProductsDetails.objects.filter(
            store__storeServicablePinCodes__contains=[201301]).get(products=pk)
        context = {
            'product': products,
            'totalcartitem': 0,
            'totalamount': a,
            'totalquantity': counter,
        }
    return render(request, "detail-page.html", context)



def searchHomePageProducts(request):
    if request.method == "GET":  # write your form name here
        product_name = request.GET.get('search')
        try:
            status = StoreProductsDetails.objects.filter(
                products__product_name__icontains=product_name)
            return render(request, "search.html", {"products": status})
        except StoreProductsDetails.DoesNotExist:
            return render(request, "search.html", {'products': status})
    else:
        return render(request, 'search.html', {'products':status})

def searchProductsInsideCategoryPage(request,pk):
    if request.method == "GET":
        product_name = request.GET.get('search')
        categorydetails = Categories.objects.get(pk=pk)
        try:
            if request.user.id != None:
                user_details = UserAddresses.objects.get(user=request.user.id)
                productdetail = StoreProductsDetails.objects.filter(products__pro_category__icontains=[
                                                                    categorydetails.category_name], products__product_name__icontains = product_name,store__storeServicablePinCodes__contains=[user_details.pincode])
                cartitems = Order.objects.get(user=request.user.id, ordered=False)
                context = {'category': categorydetails,
                        'catproducts': productdetail,
                        'totalcartitem': cartitems.get_total_items_in_order() + 1,
                        'totalamount': round(cartitems.get_total(), 2),
                        'totalquantity': cartitems.get_quantity(),
                        }
            else:
                productdetail = StoreProductsDetails.objects.filter(
                    products__pro_category__icontains=[categorydetails.category_name],products__product_name__icontains=product_name)

                context = {'category': categorydetails,
                        'catproducts': productdetail,
                        'totalcartitem': 0,
                        'totalamount': 0,
                        'totalquantity': 0,
                        }
        except Order.DoesNotExist:
            context = {
                'category': categorydetails,
                'catproducts': productdetail,
                'totalcartitem': 0,
                'totalamount': 0,
                'totalquantity': 0,
            }

    return render(request, "list.html", context)

import json
def autocompleteModel(request):
    if request.method == 'GET':
        q = request.GET.get('term', '').capitalize()
        search_qs = Products.objects.filter(product_name__startswith=q)
        results = []
        # printq
        for r in search_qs:
            results.append(r.product_name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return JsonResponse({'data':data,'application':mimetype})
