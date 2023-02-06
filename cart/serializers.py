from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, get_user_model

user = get_user_model()

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = CartSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
