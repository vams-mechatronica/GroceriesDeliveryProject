from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth
from .serializers import UpdateUserSerializer
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from products.serializer import userSerializer
from cart.models import Order

User = get_user_model()


# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print('Username exists! try another username...')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    print('Email is already taken! try another one')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    return redirect('login')   
        else:
            print('Password did not matched!..')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')        


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            print('Login Successfull!')
            return redirect('showProducts')
        else:
            print('invalid credentials')
            return redirect('login') 
    else:
        return render(request, 'accounts/login.html')           


def logout(request):
    # if request.method == 'POST':
    auth.logout(request)
        # print('logged out from websites..')
    return redirect('index')

class UpdateProfileView(generics.UpdateAPIView):
    
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user

class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = userSerializer

    def get(self,request,format = None):
        user = User.objects.get(pk=self.request.user.id)
        serializer=userSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)


def profileUser(request):
    if request.user:
        userdetails = User.objects.get(pk = request.user.id)
        context = {
            'user':userdetails
        }
    return render(request,"profile.html",context)

def userOrderDetail(request):
    if request.user:
        orders = Order.objects.filter(user = request.user.id)
        for order in orders:
            item_name = [item.item for item in order.items.all()]
            print(item_name)
        context = {
            'orders':orders
        }
    return render(request,"user-order-detail.html",context)