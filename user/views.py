from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth
from .serializers import *
from rest_framework import generics,status,permissions,authentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from products.serializer import userSerializer
from cart.models import Order
from rest_framework.decorators import api_view, permission_classes
from .models import *
from datetime import datetime,timezone
from django.http import JsonResponse
from django.utils.timezone import utc
from .utils import OTPManager
from random import randint

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
        orders = Order.objects.filter(user = request.user.id,ordered = True)
        context = {
            'orders':orders
        }
    return render(request,"user-order-detail.html",context)


def userOrderDetailExpanded(request,pk):
    if request.user:
        order_detail = Order.objects.get(user = request.user.id,pk=pk)
        print(order_detail)
    context = {
        'orders':order_detail
    }
    return render(request,"order_history.html",context)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def get_otp(request):
    try:
        # device = Device.objects.get(auth_token=request.data.get('auth_token'))
        country_code = request.data.get('country_code')
        phone_number = request.data.get('phone_number')
        fake_otp = bool(request.data.get('fake_otp'))

        try:
            last_sms = DeviceOtp.objects.filter(
                number=phone_number).latest('created_date')
            if last_sms:
                timediff = datetime.now(timezone.utc) - last_sms.created_date
                if timediff.total_seconds() < 15:
                    return JsonResponse({'Status': "Sent"})
        except Exception as e:
            print(e)
            pass

        if OTPManager.send_otp(fake_otp,
                               int(request.data.get('otp')) if fake_otp else randint(
                                   100000, 999999),
                               country_code,
                               phone_number,
                               ):
            return Response({'Status': "Sent"}, status=status.HTTP_200_OK)
        return JsonResponse({'Error': "You have exceeded your attempts."})
    except Exception as e:
        print(e)
        return Response({'Error': "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def verify_otp(request):
    try:
        # Device.objects.get(auth_token=request.data.get('auth_token'))
        phone_number = request.data.get('phone_number')
        country_code = request.data.get('country_code')
        web = bool(request.data.get('web'))
        otp = request.data.get('otp')
        print('otp is - ', otp)
        if not web:
            return OTPManager.verify_otp(otp, country_code, phone_number,web)
        else:
            user_r = OTPManager.verify_otp(otp, country_code, phone_number, web)
            auth.login(request,user_r)
            return Response({"status":"OK"},status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({'Error': "Invalid Data"}, status=status.HTTP_200_OK)


class UserAddressUpdateView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (authentication.BasicAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication)

    def get(self,request,format = None):
        address = UserAddresses.objects.get(user = request.user)
        serializer = UserAddressesSerializer(instance=address,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,format = None):
        try:
            if request.user:
                pincode = request.data.get('pincode')
                user_address,created = UserAddresses.objects.get_or_create(user=request.user,pincode=pincode)
                print(created)
                serializer = UserAddressesSerializer(instance=user_address)
                # if serializer.is_valid():
                #     return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                return Response({'data':serializer.data,'created':created}, status=status.HTTP_400_BAD_REQUEST)
            # serializer = UserAddressesSerializer(data=request.data)
            # if serializer.is_valid():
            #     instance, created = serializer.get_or_create()
            #     if not created:
            #         serializer.update(instance, serializer.validated_data)
            #     return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'data': 'Error received'}, status=status.HTTP_401_UNAUTHORIZED)
    #user,addressLine1,addressLine2,state,city,pincode

    def put(self,request,format = None):
        # address1 = request.POST.get('address1') or 'None'
        # address2 = request.POST.get('address2') or 'None'
        # state = request.POST.get('state') or 'None'
        # city = request.POST.get('city') or 'None'
        # pincode = request.data.get('pincode')
        # print(pincode)
        # alternatePhoneNumber = request.POST.get('phone_number') or 'None'
        try:
            if request.user:
                user_address = get_object_or_404(UserAddresses,user = request.user)
            serializer = UserAddressesSerializer(user_address,data = request.data,partial= True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'data':'Error received'}, status=status.HTTP_401_UNAUTHORIZED)

def address_page(request):
    addresses = UserAddresses.objects.filter(user = request.user)
    context = {'addresses':addresses}
    return render(request,"address.html",context)

            
