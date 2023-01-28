from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth
from rest_framework import generics, status, authentication, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *
from user.models import *

# Create your views here.
defaultLocationpincode = 201301

class StoreDetailsView(APIView):
    authentication_classes = [
        authentication.SessionAuthentication, authentication.TokenAuthentication]

    def get(self, request, format=None):
        stores_details = StoreDetail.objects.all()
        storeSerializer = StoreDetailSerializer(
            instance=stores_details, many=True)
        return Response(storeSerializer.data)


class StoreProductDetailsView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = (AllowAny,)

    def get(self,request,format = None):
        product_name = request.GET.get('products')
        try:
            if request.user:
                user_details = UserAddresses.objects.get(user = request.user.id)
                product_details = StoreProductsDetails.objects.filter(
                    store__storeServicablePinCodes__contains=[user_details.pincode], products__product_name__icontains=product_name)
                productDetailSerializer = StoreProductsDetailsSerializer(instance=product_details,many = True)
                return Response(productDetailSerializer.data,status=status.HTTP_200_OK)
            elif request.user == None:
                product_details = StoreProductsDetails.objects.filter(
                    store__storeServicablePinCodes__contains=[defaultLocationpincode], products__product_name__icontains=product_name)
                productDetailSerializer = StoreProductsDetailsSerializer(
                    instance=product_details, many=True)
                return Response(productDetailSerializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except UserAddresses.DoesNotExist:
            product_details = StoreProductsDetails.objects.filter(
                store__storeServicablePinCodes__contains=[defaultLocationpincode], products__product_name__icontains=product_name)
            productDetailSerializer = StoreProductsDetailsSerializer(
                instance=product_details, many=True)
            return Response(productDetailSerializer.data, status=status.HTTP_200_OK)


class StoreVerifyAtLocation(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = [authentication.BasicAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]

    def get(self,request,format=None):
        global defaultLocationpincode
        pincode = request.GET.get('pincode')
        storeAtLocationPincode = StoreDetail.objects.filter(storeServicablePinCodes__contains = [pincode])
        try:
            if len(storeAtLocationPincode) > 0:
                defaultLocationpincode = pincode
                return Response({'available':True},status=status.HTTP_200_OK)
            else:
                return Response({'available': False}, status=status.HTTP_200_OK)
        except StoreDetail.DoesNotExist:
            pass
