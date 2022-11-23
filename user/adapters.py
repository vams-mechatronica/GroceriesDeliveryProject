from allauth.account.adapter import DefaultAccountAdapter


class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_field

        user = super().save_user(request, user, form, False)
        user_field(user, 'mobileno', request.data.get('mobileno', ''))
        # user_field(user, 'address', request.data.get('address', ''))
        # user_field(user, 'first_name', request.data.get('first_name', ''))
        # user_field(user, 'last_name', request.data.get('last_name', ''))
        # user_field(user, 'user_type', request.data.get('user_type', ''))
        user.save()
        return user