# from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse,get_list_or_404,get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth,messages
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Products
from .models import *
from .serializers import *
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from stores.models import *





@login_required
def addToCart(request, pk):
    
    item = get_object_or_404(Products,pk = pk)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__product_id=item.product_id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cartview")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("cartview")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("cartview")

@login_required
def addToCartListPage(request, pk):
    
    item = get_object_or_404(StoreProductsDetails,pk = pk)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__products__product_id=item.products.product_id).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("trendingitems")
        else:
            order.items.add(order_item)
            return redirect("trendingitems")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        return redirect("trendingitems")

def cartCheckoutPageView(request):
    if request.user:
        itemsForCartPage = Cart.objects.filter(user=request.user.id,ordered = False)
    context = {
        'cartitems':itemsForCartPage
    }
    return render(request,"cart.html",context)


@login_required
def removeSingleItemFromCart(request, pk):
    item = get_object_or_404(Products, pk = pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__product_id=item.product_id).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("cartview")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("/")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("/")
