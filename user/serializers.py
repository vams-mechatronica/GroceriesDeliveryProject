# serializers.py in the users Django app
from django.db import transaction
from rest_framework import serializers
# from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import *
try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.socialaccount.helpers import complete_social_login
    from allauth.socialaccount.models import SocialAccount
    from allauth.socialaccount.providers.base import AuthProcess
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=10)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    def validate(self, data):
        mobile = data.get('mobile')
        password = data.get('password')

        if mobile and password:
            user = authenticate(request=self.context.get('request'),
                                mobile=mobile, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "mobile" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


class RegisterSerializer(serializers.Serializer):
    mobile = serializers.CharField(
        required=True,
        max_length=10,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('mobile', 'email', 'username', 'first_name',
                  'last_name', 'address', 'password1', 'password2')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate_mobileno(self, mobile):
        if mobile in User.objects.all().values_list('mobile', flat=True):
            raise serializers.ValidationError(
                _("A user is already registered with this phone number."))
        return mobile

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password1": "Password fields didn't match."})

        return attrs

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'mobile': self.validated_data.get('mobile', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        # user.mobile = self.cleaned_data.get('mobile')
        # user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'avatar')
        read_only_fields = ('email',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.username = validated_data['username']
        instance.avatar = validated_data['avatar']

        instance.save()
        return instance


class LoginOTPSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=10)
    mobile = serializers.CharField(max_length=10)
    otp = serializers.CharField(
        label=_("otp"),
        style={'input_type': 'otp'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    def validate(self, data):
        country_code = data.get('country_code')
        mobile = data.get('phone_number')
        otp = data.get('otp')
        country_id = Country.objects.get(country_code=country_code)
        device_otp = DeviceOtp.objects.get(
            number=mobile, status=True, country=country_id)

        if mobile and device_otp and int(otp) == device_otp.otp:
            user = authenticate(request=self.context.get('request'),
                                mobile=mobile)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('OTP Mismatched.')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
