# serializers.py in the users Django app
from django.db import transaction
from rest_framework import serializers
# from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

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



class CustomRegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=10)
    email = serializers.EmailField()

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.mobileno = self.data.get('phone_number')
        user.email = self.data.get('email')
        user.save()
        return user

