from django.urls import path

from . import views

urlpatterns = [
    path('accounts/register', views.register, name='register'),
    path('accounts/login', views.login, name='login'),
    path('accounts/logout', views.logout, name='logout'),
    path('accounts/update/user/profile/', views.UpdateProfileView.as_view(), name='auth_update_profile'),
    path('accounts/userprofile/',views.UserProfileView.as_view(),name="user_profile"),
    path('accounts/profilepage/',views.profileUser,name="userprofilepage"),
    path('accounts/user/ordershistory',
         views.userOrderDetail, name="orderhistoryuser"),
    path('accounts/user/ordershistory/order-detail/<int:pk>/',
         views.userOrderDetailExpanded, name="orderhistorydetail"),
    path('accounts/register/get_otp/', views.get_otp, name='get_otp'),
    path('accounts/register/verify/', views.verify_otp, name='verify_otp'),
    path('accounts/api/v1/user-address/',views.UserAddressUpdateView.as_view()),
    path('accounts/user-address',views.address_page,name="user-address-page"),
]
