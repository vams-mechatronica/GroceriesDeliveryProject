from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth,messages
from .serializers import *
from rest_framework import generics,status,permissions,authentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from products.serializer import userSerializer
from cart.models import Order
from rest_framework.decorators import api_view, permission_classes
from .models import *
from stores.models import *
from datetime import datetime,timezone
from django.http import JsonResponse
from django.utils.timezone import utc
from .utils import OTPManager
from random import randint
from django.http import Http404
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
                # print('Username exists! try another username...')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    # print('Email is already taken! try another one')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    return redirect('login')   
        else:
            # print('Password did not matched!..')
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
            # print('Login Successfull!')
            return redirect('showProducts')
        else:
            # print('invalid credentials')
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
        # print('otp is - ', otp)
        if not web:
            return OTPManager.verify_otp(otp, country_code, phone_number,web)
        else:
            user_r = OTPManager.verify_otp(otp, country_code, phone_number, web)
            auth.login(request,user_r)
            return Response({"status":"OK"},status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({'Error': "Invalid Data"}, status=status.HTTP_200_OK)


class UserAddressView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (authentication.BasicAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication)

    def get(self,request,format = None):
        address = UserAddresses.objects.filter(user = request.user)
        serializer = UserAddressesSerializer(instance=address,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,format = None):
        data = request.data
        address = data.get('address')
        add_split = address.split(",")
        
        user_address = UserAddresses()
        user_address.user = request.user
        user_address.area = add_split[0] +", "+add_split[1]
        user_address.city = add_split[2]
        user_address.pincode = add_split[3]
        user_address.save()
        
        serializer = UserAddressesSerializer(instance=user_address)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserAddressUpdateView(APIView):
    permission_classes = (IsAuthenticated, permissions.AllowAny)
    authentication_classes = (authentication.BasicAuthentication,
                              authentication.TokenAuthentication, authentication.SessionAuthentication)

    def get_object(self, pk):
        try:
            return UserAddresses.objects.get(pk=pk)
        except UserAddresses.DoesNotExist:
            raise Http404

    def get_other_objects(self,request):
        otherAddress = UserAddresses.objects.filter(user=request.user)
        serializer = UserAddressesSerializer(otherAddress, many=True)
        return serializer

    def get(self, request,pk, format=None):
        address = self.get_object(pk)
        serializer = UserAddressesSerializer(instance=address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserAddressesSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        if snippet.default_address:
            raise serializers.ValidationError({'default_address':'Primary address cannot be deleted. Please select other address as primary first'})
        else:
            snippet.delete()
        serializer = self.get_other_objects(request)
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)

def address_page(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        mobileno = request.POST.get('phone')
        houseno = request.POST.get('house_no')
        street = request.POST.get('street_address')
        landmark = request.POST.get('landmark_detail')
        area = request.POST.get('area_detail').split(",")
        area_comb = area[0]+","+area[1]
        city = request.POST.get('city_district')
        state = request.POST.get('state')
        pincode = request.POST.get('Pincode')
        nicknameaddress = request.POST.get('address_nick')
        addr = UserAddresses(user = request.user,\
            first_name = firstname,last_name = lastname,\
                mobileno=mobileno,house_no = houseno,\
                    street_detail = street,\
                        landmark=landmark,area = area_comb,city = city,\
                            pincode =pincode,state = state,\
                                address_nick_name = nicknameaddress,default_address = True)
        addr.save()
        messages.success(request,"Address saved")
    addresses = UserAddresses.objects.filter(user=request.user)
    pincode = storeServiceLocation.objects.order_by().values_list('pincode',flat=True).distinct()
    area = storeServiceLocation.objects.all()
    context = {'addresses': addresses,'store_locations':pincode,'area':area}
    return render(request, "address.html", context)

def savePartialAddressUser(request,address :str):
    add_split = address.split(",")
    add ={}
    for addr in add_split:
        if addr.isnumeric():
            add['pincode'] = addr

        elif addr.isalnum():
            add['area'] = addr
        
        elif addr.isalpha():
            add['city'] = addr
            
        else:
            add['sector'] = addr
        
    pincode = add.get('pincode') or 0
    area = add.get('area') or '' +","+ add.get('sector')

    user_address = UserAddresses()
    user_address.area = area
    user_address.pincode = pincode
    user_address.save()
    return JsonResponse({'status':'Ok'})

def delete_user_address(request,pk):
    UserAddresses.objects.filter(pk=pk).delete()
    messages.info(request,"Address has been deleted")
    return redirect("user-address-page")

        
def update_address(request,pk):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        mobileno = request.POST.get('phone')
        houseno = request.POST.get('house_no')
        street = request.POST.get('street_address')
        landmark = request.POST.get('landmark_detail')
        city = request.POST.get('city_district')
        state = request.POST.get('state')
        area = request.POST.get('area_detail')
        pincode = request.POST.get('Pincode')
        nicknameaddress = request.POST.get('address_nick')
        add = UserAddresses.objects.get(pk=pk)
        add.first_name = firstname
        add.last_name = lastname
        add.mobileno = mobileno
        add.house_no = houseno
        add.street_detail = street
        add.landmark = landmark
        add.city = city
        add.state = state
        add.address_nick_name = nicknameaddress
        add.area = area
        add.pincode = pincode
        add.save()
        messages.success(request,"Address has been updated")
        return redirect("user-address-page")
