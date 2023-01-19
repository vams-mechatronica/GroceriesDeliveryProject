from rest_framework import serializers
from stores.models import *
from django.contrib.auth import authenticate, get_user_model

user = get_user_model()

class StoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreDetail
        fields = '__all__'

class StoreProductsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreProductsDetails
        fields = "__all__"