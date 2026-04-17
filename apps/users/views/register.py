from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.shared.utils.custom_response import CustomResponse
from apps.users.serializers.register import RegisterSerializer
from apps.users.utils.verification_code import (
    generate_verification_code,
    send_verification_code,
)

VERIFICATION_CODE_TIMEOUT = 120


def _verification_cache_key(user_id):
    return f"user_verification_code:{user_id}"


def _save_verification_code(user_id, code):
    cache.set(_verification_cache_key(user_id), code, timeout=VERIFICATION_CODE_TIMEOUT)


def _get_verification_code(user_id):
    return cache.get(_verification_cache_key(user_id))


def _delete_verification_code(user_id):
    cache.delete(_verification_cache_key(user_id))


def _get_identifier(request):
    return request.data.get("phone_number") or request.data.get("username")


def _get_user(identifier):
    user_model = get_user_model()
    model_fields = {field.name for field in user_model._meta.get_fields()}

    filters = Q()
    has_lookup_field = False
    if "phone_number" in model_fields:
        filters |= Q(phone_number=identifier)
        has_lookup_field = True
    if "username" in model_fields:
        filters |= Q(username=identifier)
        has_lookup_field = True

    if not has_lookup_field:
        raise user_model.DoesNotExist

    return user_model.objects.get(filters)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                request=request,
                errors=serializer.errors,
            )

        user = serializer.save()
        code = generate_verification_code()

        _save_verification_code(user.id, code)
        send_verification_code(user, code)

        return CustomResponse.success(
            request=request,
            data=serializer.data,
            message_key="USER_REGISTERED_SUCCESSFULLY",
        )


class VerifyCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = _get_identifier(request)
        code = request.data.get("code")
        user_model = get_user_model()

        if not identifier or not code:
            return Response(
                {"error": "phone_number or username and code are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = _get_user(identifier)
        except user_model.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        saved_code = _get_verification_code(user.id)
        if saved_code is None:
            return Response(
                {"error": "Verification code expired or not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if str(saved_code) != str(code):
            return Response(
                {"error": "Verification code is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = True
        user.save(update_fields=["is_active"])
        _delete_verification_code(user.id)

        return Response(
            {"message": "User verified successfully"},
            status=status.HTTP_200_OK,
        )


class ResendVerificationCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = _get_identifier(request)
        user_model = get_user_model()

        if not identifier:
            return Response(
                {"error": "phone_number or username is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = _get_user(identifier)
        except user_model.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        code = generate_verification_code()
        _save_verification_code(user.id, code)
        send_verification_code(user, code)

        return Response(
            {"message": "A new verification code has been sent"},
            status=status.HTTP_200_OK,
        )
