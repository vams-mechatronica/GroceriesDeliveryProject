# serializers.py in the users Django app
from django.db import transaction
from rest_framework import serializers
# from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
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
    mobileno = serializers.CharField(max_length=10)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    def validate(self, data):
        mobileno = data.get('mobileno')
        password = data.get('password')

        if mobileno and password:
            user = authenticate(request=self.context.get('request'),
                                mobileno=mobileno, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "mobileno" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data

class RegisterSerializer(serializers.Serializer):
    mobileno = serializers.CharField(
                required = True,
                max_length = 10,
                validators =[UniqueValidator(queryset=User.objects.all())]
                )
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('mobileno','email','username','first_name', 'last_name','address', 'password1', 'password2')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    def validate_mobileno(self,mobileno):
        if mobileno in User.objects.all().values_list('mobileno',flat=True):
            raise serializers.ValidationError(
                    _("A user is already registered with this phone number."))
        return mobileno
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
            raise serializers.ValidationError({"password1": "Password fields didn't match."})

        return attrs

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'mobileno': self.validated_data.get('mobileno', ''),
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
        # user.mobileno = self.cleaned_data.get('mobileno')
        # user.save()
        return user

class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'address','avatar')
        read_only_fields = ('email',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.username = validated_data['username']
        instance.address = validated_data['address']
        instance.avatar = validated_data['avatar']

        instance.save()
        return instance