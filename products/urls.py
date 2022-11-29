from django.urls import path
from .views import *

urlpatterns = [
    path("products/", ProductDetails.as_view(), name="allproducts"),
]
