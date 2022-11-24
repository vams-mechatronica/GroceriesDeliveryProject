from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('update/user/profile/', views.UpdateProfileView.as_view(), name='auth_update_profile'),
   
]