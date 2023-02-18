from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("products/", ProductDetails.as_view(), name="allproducts"),
    path('',index,name="index"),
    path("seeallproducts/<int:pk>",seeAllProductsInCategory,name="seeallproductsincategory"),
    path("productdetail/<int:pk>",productDetailsPageView,name="productdetail"),
    # path("products/search/", searchHomePageProducts, name="productsearch"),
    path("products/search/", autocompleteModel, name="productsearch"),
    path("products/search/categories/<int:pk>",searchProductsInsideCategoryPage,name="productsearchcategory"),
    path('about-us', about, name="about"),
    path('terms-conditions', term, name="terms_conditions"),
    path('privacy-policy', privacy, name="privacy_policy"),
    path('cookies-policy', cookie, name="cookies_policy"),
    path('contact-us', contact, name="contact_us"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
