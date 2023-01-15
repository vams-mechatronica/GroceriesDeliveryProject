from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("addtocart/<int:pk>",addToCart,name="addtocart"),
    path("checkout/",cartCheckoutPageView,name="cartview"),
    path("removesingleitemfromcart/<int:pk>",removeSingleItemFromCart,name="removesingleitemfromcart")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)