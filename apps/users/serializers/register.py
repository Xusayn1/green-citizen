import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.models import Language
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
