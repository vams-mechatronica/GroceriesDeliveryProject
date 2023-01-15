from django.urls import path,register_converter
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .utils import FloatConverter

# register_converter(converters.RomanNumeralConverter, 'roman')
register_converter(FloatConverter, 'float')

urlpatterns = [
    path("addtocart/<int:pk>",addToCart,name="addtocart"),
    path("ordersummary/",cartCheckoutPageView,name="cartview"),
    path("removesingleitemfromcart/<int:pk>",removeSingleItemFromCart,name="removesingleitemfromcart"),
    path("payment/checkout/<float:amount>",orderPaymentRequest,name="paymentcheckout"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)