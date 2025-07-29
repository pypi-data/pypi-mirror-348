from rest_framework import serializers


class PassportUserSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField(required=True, allow_null=False)
    user_auth_code = serializers.CharField(
        max_length=255, required=True, allow_null=False
    )


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        required=True, allow_null=False
    )


class FullAccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        required=True, allow_null=False
    )
    access_token_expiration = serializers.DateTimeField(required=True, allow_null=False)


class TokenExchangeRequestSerializer(PassportUserSerializer):
    """
    Data from passport server from the 1st part of the exchange flow
    """

    email = serializers.EmailField(max_length=255, required=True, allow_null=False)
    username = serializers.CharField(max_length=255, required=True, allow_null=False)
    country_iso = serializers.CharField(max_length=10, required=False, allow_null=True)


class TokenExchangeCompleteSerializer(
    PassportUserSerializer, FullAccessTokenSerializer
):
    """
    Date from passport. The last step of the exchange flow.
    All information about user and tokens
    """

    refresh_token = serializers.CharField(
        required=True, allow_null=False
    )


class ServiceKeySerializer(serializers.Serializer):
    """
    Serializer for get_service_key endpoint
    """

    service_key = serializers.CharField(max_length=255, required=True, allow_null=False)


class TokenExchangeResponseSerializer(PassportUserSerializer, ServiceKeySerializer):
    """
    Data from our service to passport as the part of the exchange flow. Request fi
    """

    pass

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PassportUserSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField(required=True, allow_null=False)
    user_auth_code = serializers.CharField(
        max_length=255, required=True, allow_null=False
    )


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        required=True, allow_null=False
    )


class FullAccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        required=True, allow_null=False
    )
    access_token_expiration = serializers.DateTimeField(required=True, allow_null=False)


class ServiceKeySerializer(serializers.Serializer):
    """
    Serializer for get_service_key endpoint
    """

    service_key = serializers.CharField(max_length=255, required=True, allow_null=False)


class ExtraTokenRequestSerializer(serializers.Serializer):
    """
    Data to get android token
    """
    token_target = serializers.CharField(max_length=255, required=True)


class UpdateUserInfoSerializer(serializers.Serializer):
    old_email = serializers.EmailField(max_length=255, required=False, allow_null=True)
    new_email = serializers.CharField(max_length=255, required=False, allow_null=True)
    is_email_verified = serializers.BooleanField(required=False, default=True)
    exchange_key = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["exchange_key"] != settings.PASSPORT_EXCHANGE_KEY:
            raise ValidationError("Wrong exchange_key")
        return attrs


class UpdateUserInfoSerializer(serializers.Serializer):
    old_email = serializers.EmailField(max_length=255, required=False, allow_null=True)
    new_email = serializers.CharField(max_length=255, required=False, allow_null=True)
    is_email_verified = serializers.BooleanField(required=False, default=True)
    exchange_key = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["exchange_key"] != settings.PASSPORT_EXCHANGE_KEY:
            raise ValidationError("Wrong exchange_key")
        return attrs
