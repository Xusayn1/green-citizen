from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class MultiFieldBackend(ModelBackend):
    """
    Authentication backend that allows login with email, username, or phone_number
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            # Try to find user by email, username
            user = user_model.objects.get(
                Q(email__iexact=username) |
                Q(username__iexact=username) |
                Q(phone_number__iexact=username)
            )

            if user.check_password(password) and user.is_active:
                return user
        except user_model.DoesNotExist:
            pass
        return None
