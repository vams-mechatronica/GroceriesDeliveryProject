from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth
from rest_framework import generics, status, authentication, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *

# Create your views here.


class StoreDetailsView(APIView):
    authentication_classes = [
        authentication.SessionAuthentication, authentication.TokenAuthentication]

    def get(self, request, format=None):
        stores_details = StoreDetail.objects.all()
        storeSerializer = StoreDetailSerializer(
            instance=stores_details, many=True)
        return Response(storeSerializer.data)
