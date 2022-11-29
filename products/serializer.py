from rest_framework import serializers
from .models import *

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image_id','images']

class ProductReviewAndRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviewAndRatings
        fields = ['review','ratings','upload_image','author']
    
class ProductsSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many = True, read_only = True)
    reviews = ProductReviewAndRatingsSerializer(many = True, read_only = True)
    class Meta:
        model = Products
        fields = '__all__'