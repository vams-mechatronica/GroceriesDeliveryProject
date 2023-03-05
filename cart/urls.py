from django.urls import path,register_converter
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .utils import FloatConverter

# register_converter(converters.RomanNumeralConverter, 'roman')
register_converter(FloatConverter, 'float')

urlpatterns = [
    path("addtocart/<int:pk>/",addToCart,name="addtocart"),
    path("ordersummary/",cartCheckoutPageView,name="cartview"),
    path("removesingleitemfromcart/<int:pk>/",removeSingleItemFromCart,name="removesingleitemfromcart"),
    path("payment/checkout/<float:amount>/",orderPaymentRequest,name="paymentcheckout"),
    path("paymentstatusupdate/",paymentStatusAndOrderStatusUpdate,name="paymentstatusupdate"),
    path("order-summary/<int:pk>/",order_summary,name="ordersummary"),
    path("api/v1/customer/order/add/",
         CartAddView.as_view(), name="addtocartapi"),
    path("api/v1/customer/order/remove/",
         CartRemoveView.as_view(), name="removetocartapi"),
     path("payment-pending/<int:pk>/",pending_payment_page,name="pending-payment"),
    path("payment-failed/<int:pk>/",
         failed_payment_page, name="failed-payment"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
