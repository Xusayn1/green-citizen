from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.shared.utils.custom_response import CustomResponse
from apps.users.serializers.register import (
    LoginSerializer,
    MeSerializer,
    RegisterSerializer,
    ResendVerificationCodeSerializer,
    SetPasswordSerializer,
    UpdatePasswordSerializer,
    UpdatePhoneNumberSerializer,
    UpdateUserSerializer,
    VerifyCodeSerializer,
    VerifyUpdateCodeSerializer,
)
from apps.users.utils.verification_code import send_verification_code


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=str(serializer.errors),
                message_key="VALIDATION_ERROR"
            )
        user = serializer.save()

        # send verification code to the user's phone number
        send_verification_code.delay(user.id)

        tokens = user.get_tokens()
        data = {
            "user": serializer.data,
            "tokens": tokens
        }

        return CustomResponse.success(
            request=request,
            data=data,
            message_key="USER_REGISTERED_SUCCESSFULLY"
        )


class VerifyCodeAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyCodeSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=str(serializer.errors),
                message_key="VALIDATION_ERROR"
            )
        user = serializer.save()

        tokens = user.get_tokens()
        data = {
            "user": serializer.data,
            "tokens": tokens
        }

        return CustomResponse.success(
            request=request,
            data=data,
            message_key="CODE_VERIFIED_SUCCESSFULLY"
        )


class ResendVerificationCodeAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResendVerificationCodeSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=str(serializer.errors),
                message_key="VALIDATION_ERROR"
            )
        user = serializer.save()

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=str(serializer.errors),
                message_key="VALIDATION_ERROR"
            )
        user = serializer.save()

        tokens = user.get_tokens()
        data = {
            "user": serializer.data,
            "tokens": tokens
        }

        return CustomResponse.success(
            request=request,
            data=data,
            message_key="LOGIN_SUCCESSFULLY"
        )


class UpdatePasswordAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UpdatePasswordSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=str(serializer.errors),
                message_key="VALIDATION_ERROR"
            )
        user = serializer.save()

        tokens = user.get_tokens()
        data = {
            "user": serializer.data,
            "tokens": tokens
        }

        return CustomResponse.success(
            request=request,
            data=data,
            message_key="PASSWORD_UPDATED_SUCCESSFULLY"
        )


class UpdatePhoneNumberAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UpdatePhoneNumberSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=str(serializer.errors),
                message_key="VALIDATION_ERROR"
            )
        user = serializer.save()
        send_verification_code.delay(user.id)
        data = {"user": serializer.data}

        return CustomResponse.success(
            request=request,
            data=data,
            message_key="PHONE_NUMBER_UPDATED_SUCCESSFULLY"
        )


class VerifyUpdateCodeAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyUpdateCodeSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=str(serializer.errors),
                message_key="VALIDATION_ERROR"
            )
        user = serializer.save()

        tokens = user.get_tokens()
        data = {
            "user": serializer.data,
            "tokens": tokens
        }   

        return CustomResponse.success(
            request=request,
            data=data,
            message_key="UPDATE_CODE_VERIFIED_SUCCESSFULLY"
        )


class UpdateUserAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UpdateUserSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data, partial=True, context={"request": request})
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=str(serializer.errors),
                message_key="VALIDATION_ERROR"
            )
        user = serializer.save()
        data = self.serializer_class(user).data
        return CustomResponse.success(
            request=request,
            data=data,
            message_key="USER_UPDATED_SUCCESSFULLY"
        )


class SetPasswordAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SetPasswordSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=str(serializer.errors),
                message_key="VALIDATION_ERROR"
            )
        user = serializer.save()
        tokens = user.get_tokens()
        data = {
            "user": serializer.data,
            "tokens": tokens
        }
        return CustomResponse.success(
            request=request,
            data=data,
            message_key="PASSWORD_SET_SUCCESSFULLY"
        )

class MeAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = MeSerializer
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return CustomResponse.success(
            request=request,
            data=serializer.data,
            message_key="USER_DETAILS_SUCCESSFULLY"
        ) 

