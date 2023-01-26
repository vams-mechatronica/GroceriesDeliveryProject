from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, get_user_model

user = get_user_model()

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['first_name','last_name','username','email','avatar']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('category_name',)

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image_id','images']

class ProductReviewAndRatingsSerializer(serializers.ModelSerializer):
    author = userSerializer()
    class Meta:
        model = ProductReviewAndRatings
        fields = ['review','ratings','upload_image','author']
    
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        exclude = ('desc',)