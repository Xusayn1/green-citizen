import re

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.models import Language
from apps.users.models.users import VerificationCode
from apps.users.utils.generate_password import generate_password

try:
    import phonenumbers
except ImportError:  # pragma: no cover - optional dependency
    phonenumbers = None

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    language = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["phone_number", "language"]

    @staticmethod
    def validate_phone_number(phone_number):
        normalized_phone_number = RegisterSerializer._normalize_phone_number(phone_number)

        if User.objects.filter(phone_number=normalized_phone_number).exists():
            raise CustomException(
                message_key="PHONE_NUMBER_EXIST_ERROR",
                context={"phone_numbers": normalized_phone_number},
            )

        return normalized_phone_number

    @staticmethod
    def _normalize_phone_number(phone_number):
        if phonenumbers:
            try:
                parsed = phonenumbers.parse(phone_number, None)
            except phonenumbers.NumberParseException:
                raise CustomException(
                    message_key="INVALID_PHONE_NUMBER_ERROR",
                    context={"phone_numbers": phone_number},
                )

            if not phonenumbers.is_valid_number(parsed):
                raise CustomException(
                    message_key="INVALID_PHONE_NUMBER_ERROR",
                    context={"phone_numbers": phone_number},
                )

            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)

        sanitized = re.sub(r"[^\d+]", "", phone_number.strip())
        if not sanitized.startswith("+"):
            raise CustomException(
                message_key="INVALID_PHONE_NUMBER_ERROR",
                context={"phone_numbers": phone_number},
            )

        digits_only = sanitized[1:]
        if not digits_only.isdigit() or not 8 <= len(digits_only) <= 15:
            raise CustomException(
                message_key="INVALID_PHONE_NUMBER_ERROR",
                context={"phone_numbers": phone_number},
            )

        return f"+{digits_only}"

    @staticmethod
    def validate_language(language):
        if language not in Language.values:
            raise CustomException(message_key="INVALID_LANGUAGE_TYPE")
        return language

    def create(self, validated_data):
        phone_number = validated_data.get("phone_number")
        language = validated_data.get("language", Language.EN)
        password = generate_password()
        return User.objects.create_user(
            phone_number=phone_number,
            password=password,
            language=language,
        )


class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate_phone_number(self, value):
        return RegisterSerializer._normalize_phone_number(value)

    def validate(self, attrs):
        attrs["user"] = User.objects.filter(phone_number=attrs["phone_number"]).first()
        if not attrs["user"]:
            raise CustomException(message_key="USER_NOT_FOUND")
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.is_active = True
        user.save(update_fields=["is_active", "updated_at"])
        return user


class ResendVerificationCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def validate_phone_number(self, value):
        return RegisterSerializer._normalize_phone_number(value)

    def validate(self, attrs):
        user = User.objects.filter(phone_number=attrs["phone_number"]).first()
        if not user:
            raise CustomException(message_key="USER_NOT_FOUND")
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        return self.validated_data["user"]


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate_phone_number(self, value):
        return RegisterSerializer._normalize_phone_number(value)

    def validate(self, attrs):
        user = authenticate(
            username=attrs["phone_number"],
            password=attrs["password"],
        )
        if not user:
            raise CustomException(message_key="INVALID_CREDENTIALS")
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        return self.validated_data["user"]


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password1 = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.is_authenticated:
            raise CustomException(message_key="UNAUTHORIZED")
        if not user.check_password(attrs["old_password"]):
            raise CustomException(message_key="INVALID_OLD_PASSWORD")
        if attrs["new_password1"] != attrs["new_password2"]:
            raise CustomException(message_key="PASSWORDS_DO_NOT_MATCH")
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password1"])
        user.save(update_fields=["password", "updated_at"])
        return user


class UpdatePhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def validate_phone_number(self, value):
        normalized_phone = RegisterSerializer._normalize_phone_number(value)
        if User.objects.filter(phone_number=normalized_phone).exists():
            raise CustomException(
                message_key="PHONE_NUMBER_EXIST_ERROR",
                context={"phone_numbers": normalized_phone},
            )
        return normalized_phone

    def save(self, **kwargs):
        return self.context["request"].user


class VerifyUpdateCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate_phone_number(self, value):
        return RegisterSerializer._normalize_phone_number(value)

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.is_authenticated:
            raise CustomException(message_key="UNAUTHORIZED")
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.phone_number = self.validated_data["phone_number"]
        user.save(update_fields=["phone_number", "updated_at"])
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "middle_name", "email", "language"]

    def save(self, **kwargs):
        user = self.context["request"].user
        if not user.is_authenticated:
            raise CustomException(message_key="UNAUTHORIZED")
        for field, value in self.validated_data.items():
            setattr(user, field, value)
        user.save()
        return user


class SetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_phone_number(self, value):
        return RegisterSerializer._normalize_phone_number(value)

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise CustomException(message_key="PASSWORDS_DO_NOT_MATCH")
        user = User.objects.filter(phone_number=attrs["phone_number"]).first()
        if not user:
            raise CustomException(message_key="USER_NOT_FOUND")
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["password1"])
        user.save(update_fields=["password", "updated_at"])
        return user


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "language",
        ]
