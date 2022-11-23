from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def _create_user(self, mobileno, email, password, **extra_fields):
        if not mobileno:
            raise ValueError(_('Users must have an active mobile number'))
        email = self.normalize_email(email)
        user = self.model(mobileno=mobileno, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, mobile, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, email, password, **extra_fields)

    def create_superuser(self, mobileno, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self._create_user(mobileno, email, password, **extra_fields)