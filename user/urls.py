from django.urls import path

from . import views

urlpatterns = [
    path('accounts/register', views.register, name='register'),
    path('accounts/login', views.login, name='login'),
    path('accounts/logout', views.logout, name='logout'),
    path('accounts/update/user/profile/', views.UpdateProfileView.as_view(), name='auth_update_profile'),
    path('accounts/userprofile/',views.UserProfileView.as_view(),name="user_profile"),
    path('accounts/profilepage',views.profileUser,name="userprofilepage"),
    path('accounts/user/ordershistory',views.userOrderDetail,name="orderhistoryuser"),
]