from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("products/", ProductDetails.as_view(), name="allproducts"),
    path('',index,name="index"),
    path("seeallproducts/<int:pk>",seeAllProductsInCategory,name="seeallproductsincategory"),
    path("productdetail/<int:pk>",productDetailsPageView,name="productdetail"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)