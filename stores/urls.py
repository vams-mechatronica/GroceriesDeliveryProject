from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("stores/store-detail/",StoreDetailsView.as_view()),
    path("stores/products/",StoreProductDetailsView.as_view()),
    path("stores/availability/", StoreVerifyAtLocation.as_view()),
    path("stores/suggest-delivery-location/",SuggestVerifyDeliveryLocation.as_view()),
    path("contact-us/form/",contact_us_form,name="form-contact-us"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
