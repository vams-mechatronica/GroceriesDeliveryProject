from django.http import JsonResponse
from .models import DeviceOtp, Country
from django.http import JsonResponse
from datetime import date
from django.contrib import auth
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
import requests
from .serializers import UserSerializer
from django.contrib.auth import authenticate, get_user_model

user_model = get_user_model()


class OTPManager:
    @staticmethod
    def send_otp(fake_otp, otp, country_code, phone_number):
        print(otp)
        count = DeviceOtp.objects.filter(
            number=phone_number, created_date__date=date.today()).count()
        if count > 5:
            return False
        try:
            device_otps = DeviceOtp.objects.filter(
                number=phone_number, status=True)
            for device_otp in device_otps:
                device_otp.status = False
                device_otp.save()
        except Exception as e:
            print(e)
            pass

        country_code = country_code.replace('+', '')

        country = Country.objects.filter(
            country_code__contains=country_code)[0]
        if not fake_otp:
            msgtxt = str(otp) + ' is the OTP for Glovo Food Delivery App.'
            msgtxt = msgtxt.replace(" ", "%20")
            # url = "https://9rd3vd.api.infobip.com/sms/1/text/query?username=MudStudio&password=Prune@2022&from=IPrune&to=91" + \
            #     phone_number+"&indiaDltContentTemplateId=1107161513294569922&indiaDltPrincipalEntityId=1101439040000040339&text="+msgtxt
            # x = requests.get(url)

        DeviceOtp.objects.create(
            number=phone_number, otp=otp, status=True, country=country)
        return True

    @staticmethod
    def verify_otp(otp, country_code, phone_number,web):
        country_code = country_code.replace('+', '')
        country = Country.objects.get(country_code=country_code)
        device_otp = DeviceOtp.objects.get(
            number=phone_number, status=True, country=country)
        if int(otp) != device_otp.otp:
            return JsonResponse({'Error': "OTP Didn't matched!"}, status=status.HTTP_401_UNAUTHORIZED)
        user, created = user_model.objects.get_or_create(mobileno=phone_number)
        token, created = Token.objects.get_or_create(user=user)
        if web == False:
            device_otp.status = False
            device_otp.save()
            return JsonResponse({'user': UserSerializer(user).data, 'token': token.key},status=status.HTTP_201_CREATED)
        else:
            device_otp.status = False
            device_otp.save()
            return user
    # @staticmethod
    # def verify_otp_new(otp, country_code, phone_number):
    #     country = Country.objects.get(country_code=country_code)
    #     device_otp = DeviceOtp.objects.get(
    #         number=phone_number, status=True, country=country)
    #     if int(otp) != device_otp.otp:
    #         return JsonResponse({'Error': "OTP Didn't matched!"}, status=status.HTTP_200_OK)

    # @staticmethod
    # def success_paid(message, type, phone_number):
    #     if type == 'billpayment':
    #         try:
    #             phone_number = str(phone_number)
    #             msgtxt = str(message)
    #             msgtxt = msgtxt.replace(" ", "%20")
    #             url = "https://9rd3vd.api.infobip.com/sms/1/text/query?username=MudStudio&password=Prune@2022&from=UPrune&to=91" + \
    #                 phone_number+"&indiaDltContentTemplateId=1107165754352622776&indiaDltPrincipalEntityId=1101439040000040339&text="+msgtxt
    #             x = requests.get(url)
    #             print(x.text)

    #         except Exception as e:
    #             print(e)
    #     elif type == 'sim_order':
    #         try:
    #             phone_number = str(phone_number)
    #             msgtxt = str(message)
    #             msgtxt = msgtxt.replace(" ", "%20")
    #             url = "https://9rd3vd.api.infobip.com/sms/1/text/query?username=MudStudio&password=Prune@2022&from=IPrune&to=91" + \
    #                 phone_number+"&indiaDltContentTemplateId=1107165754352622776&indiaDltPrincipalEntityId=1101439040000040339&text="+msgtxt
    #             new_url = url.replace("%26", "&")
    #             x = requests.get(new_url)
    #             print(new_url)

    #         except Exception as e:
    #             print(e)
