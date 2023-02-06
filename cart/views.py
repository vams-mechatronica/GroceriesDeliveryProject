# from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse, get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth, messages
from rest_framework import generics, status,authentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Products
from .models import *
from .serializers import *
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from stores.models import *
from user.models import UserAddresses
from instamojo_wrapper import Instamojo
api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')

User = get_user_model()


@login_required
def addToCart(request, pk):

    if request.user:
        try:
            user_details = UserAddresses.objects.get(user=request.user.id)
            item = get_object_or_404(StoreProductsDetails, products=pk,
                             store__storeServicablePinCodes__contains=[user_details.pincode])
        except UserAddresses.DoesNotExist:
            item = get_object_or_404(StoreProductsDetails, products=pk,
                                     store__storeServicablePinCodes__contains=[201301])
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__products__product_id=item.products.product_id).exists() and item.available_stock > 0:
            order_item.quantity += 1
            item.available_stock = item.available_stock - 1
            item.save()
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cartview")
        elif item.available_stock > 0:
            order.items.add(order_item)
            item.available_stock = item.available_stock - 1
            item.save()
            messages.info(request, "This item was added to your cart.")
            return redirect("cartview")
        else:
            messages.info(request, "Item Out of Stock")
            return redirect("/")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("cartview")


# @login_required
def cartCheckoutPageView(request):
    counter = 0
    a = 0
    b = 0
    
    try:
        if request.user:
            itemsForCartPage = Order.objects.get(
                user=request.user.id, ordered=False)

        a = round(itemsForCartPage.get_total(), 2)
        counter = len(itemsForCartPage.items.all())

        if a > 500:
            delivery_charges = 0
        else:
            delivery_charges = 0

        grandtotal = a + delivery_charges

        context = {
            'object': itemsForCartPage,
            'delivery': delivery_charges,
            'totalquantity': counter,
            'grandtotal': grandtotal
        }
    
    except Order.DoesNotExist:

        if a > 500:
            delivery_charges = 0
        else:
            delivery_charges = 0

        grandtotal = a + delivery_charges

        context = {
            'object': [],
            'delivery': delivery_charges,
            'useraddress': "",
            'totalquantity': counter,
            'grandtotal': grandtotal
        }
    
    return render(request, "cart.html", context)


@login_required
def removeSingleItemFromCart(request, pk):
    if request.user:
        try:
            user_details = UserAddresses.objects.get(user=request.user.id)
            item = get_object_or_404(StoreProductsDetails, products=pk,
                                store__storeServicablePinCodes__contains=[user_details.pincode])
        except UserAddresses.DoesNotExist:
            item = get_object_or_404(StoreProductsDetails, products=pk,
                                     store__storeServicablePinCodes__contains=[201301])

    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__products__product_id=item.products.product_id).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                item.available_stock += 1
                item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
                item.available_stock += 1
                item.save()
            # messages.info(request, "This item quantity was updated.")
            return redirect("cartview")
        else:
            # messages.info(request, "This item was not in your cart")
            return redirect("/")
    else:
        # messages.info(request, "You do not have an active order")
        return redirect("/")


@login_required
def orderPaymentRequest(request, amount):
    if request.user:
        user = User.objects.get(pk=request.user.id)
        order = Order.objects.get(user=request.user.id, ordered=False)
    response = api.payment_request_create(
        amount=str(amount),
        purpose='test_purchase',
        buyer_name=user.username or None,
        send_sms=settings.SEND_SMS,
        send_email=settings.SEND_EMAIL,
        email=user.email or None,
        phone=user.mobileno,
        redirect_url=settings.PAYMENT_SUCCESS_REDIRECT_URL,
        allow_repeated_payments=False
    )
    # print(response)
    order.ref_code = response['payment_request']['id']
    order.save()
    payment_redirect_url = response['payment_request']['longurl']
    if payment_redirect_url:
        context = {
            'payment_url': payment_redirect_url
        }
        return render(request, "paymentredirect.html", context)
    else:
        return redirect("cartview")


@login_required
def paymentStatusAndOrderStatusUpdate(request):
    if request.user:
        user = User.objects.get(pk=request.user.id)
        order = Order.objects.get(user=request.user.id, ordered=False)
        # cartItems = Cart.objects.filter(user = request.user.id,ordered = False)
        # for order in orders:
        if order.ref_code:
            payment_status = api.payment_request_status(order.ref_code)
            if payment_status['payment_request']['status'] == 'Completed':
                # cartItems.ordered = True
                # cartItems.save()
                order.ordered = True
                payment = Payment()
                payment.instamojo_id = payment_status['payment_request']['payments'][0]['payment_id']
                payment.user = request.user
                payment.amount = payment_status['payment_request']['payments'][0]['amount']
                payment.save()

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.payment = payment
                order.save()
            messages.success(request, "Your order was successful!")
    return redirect("ordersummary", pk=order.id)

@login_required
def order_summary(request,pk):
    if request.user:
        order = Order.objects.get(user=request.user.id, pk=pk)
       
    context = {
        'order': order
    }
    return render(request, "ordersummary.html", context)


class CartAddView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (authentication.BasicAuthentication,
                              authentication.SessionAuthentication, authentication.TokenAuthentication)

    def get(self, request, format=None):
        try:
            itemsForCartPage = Order.objects.get(
                user=request.user.id, ordered=False)
            serializer = OrderSerializer(instance=itemsForCartPage, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'cart': 'No items in cart'}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        data = request.data
        product_pk = data.get('product')
        quantity = int(data.get('quantity'))
        
        try:
            user_details = UserAddresses.objects.get(user=request.user.id)
            item = get_object_or_404(StoreProductsDetails, products=product_pk,
                                     store__storeServicablePinCodes__contains=[user_details.pincode])
        except UserAddresses.DoesNotExist:
            item = get_object_or_404(StoreProductsDetails, products=product_pk,
                                     store__storeServicablePinCodes__contains=[201301])

        order_item, created = Cart.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__id=item.id).exists() and item.available_stock > 0:
                order_item.quantity += quantity
                item.available_stock = item.available_stock - quantity
                item.save()
                order_item.save()

            elif item.available_stock > 0:
                order.items.add(order_item)
                item.available_stock = item.available_stock - quantity
                item.save()
            else:
                return Response({'cart': 'Item out of Stock'}, status=status.HTTP_200_OK)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
        serializer = OrderSerializer(instance=order_qs, many=True)
        return Response({'cart': serializer.data}, status=status.HTTP_200_OK)
