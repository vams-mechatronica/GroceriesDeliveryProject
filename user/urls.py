from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
     path("register/",include("dj_rest_auth.registration.urls")),
    path('web-register', views.register, name='register'),
    path('web-login', views.login, name='login'),
    path('web-logout', views.logout, name='logout'),
    path('update/user/profile/', views.UpdateProfileView.as_view(), name='auth_update_profile'),
    path('userprofile/',views.UserProfileView.as_view(),name="user_profile"),
    path('profilepage/',views.profileUser,name="userprofilepage"),
    path('user/ordershistory',
         views.userOrderDetail, name="orderhistoryuser"),
    path('email-verification/', include('verify_email.urls')),
    path('user/ordershistory/order-detail/<int:pk>/',
         views.userOrderDetailExpanded, name="orderhistorydetail"),
    path('register/get_otp/', views.get_otp, name='get_otp'),
    path('register/verify/', views.verify_otp, name='verify_otp'),
    path('api/v1/user-address/', views.UserAddressView.as_view()),
    path('api/v1/user-address/<int:pk>/', views.UserAddressUpdateView.as_view()),
    path('user-address/', views.address_page, name="user-address-page"),
    path('user-address/delete/<int:pk>',
         views.delete_user_address, name="delete-address"),
    path('user-address/save-partial/<str:address>',views.savePartialAddressUser,name="save-partial-address"),
    path('user-address/update/<int:pk>/',views.update_address,name='user-address-update'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
