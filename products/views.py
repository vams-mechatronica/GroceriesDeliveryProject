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

User = get_user_model()

# Create your views here.
class ProductDetails(APIView):
    permission_classes = (AllowAny,)
    def get(self, req, format=None):
        tbl_product = Products.objects.all()
        serializer = ProductsSerializer(instance=tbl_product, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)