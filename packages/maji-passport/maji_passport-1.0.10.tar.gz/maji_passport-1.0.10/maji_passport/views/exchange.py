import re
from urllib.parse import urlencode

import loguru
from django.conf import settings
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from maji_passport.authentication.backend import PassportAuthBackendMainEndpoint, PassportExpireTokenBackend
from maji_passport.hooks import on_update_user
from maji_passport.serializers.exchange import (
    TokenExchangeRequestSerializer,
    ServiceKeySerializer,
    AccessTokenSerializer,
    UpdateUserInfoSerializer,
)
from maji_passport.services.auth import RSAPassportService
from maji_passport.services.exchange import ExchangeTokenService
from maji_passport.services.proxy import PassportProxy

User = get_user_model()


class ExchangeTokenViewSet(GenericViewSet):
    serializer_class = TokenExchangeRequestSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=AccessTokenSerializer,
        responses={204: AccessTokenSerializer()},
    )
    @action(
        detail=False,
        methods=["POST"],
    )
    def update_token(self, request):
        """
        Made server-server request for update token
        """
        serializer = AccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.data["access_token"]
        params = {
            "service_key": settings.PASSPORT_SERVICE_KEY,
        }
        backwards_url = request.GET.get("backwards_url", None)
        if backwards_url:
            params["backwards_url"] = backwards_url

        response_dict = ExchangeTokenService.send_post_request(
            settings.PASSPORT_UPDATE_TOKEN_URL + "?" + urlencode(params),
            {},
            headers={"Authorization": f"Bearer {token}"},
        )
        return Response(response_dict, status=status.HTTP_200_OK)


class UpdateTokenV2(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Made server-server request for update token v2. Take token from headers
        """
        token = request.headers.get("Authorization")
        if not token:
            return None, None
        params = {
            "service_key": settings.PASSPORT_SERVICE_KEY,
        }
        backwards_url = request.query_params.get("backwards_url", None)
        if backwards_url:
            params["backwards_url"] = backwards_url

        response_dict = ExchangeTokenService.send_post_request(
            settings.PASSPORT_UPDATE_TOKEN_URL + "?" + urlencode(params),
            {},
            headers={"Authorization": token},
        )
        # update token in service
        new_token = response_dict.get("access_token")
        RSAPassportService.update_access_token(new_token)
        return Response(response_dict, status=status.HTTP_200_OK)


class ServiceToken(GenericViewSet):
    @swagger_auto_schema(
        responses={200: ServiceKeySerializer()},
    )
    @action(detail=False, methods=["get"])
    def get_service_key(self, request):
        """
        Get service token for exchange data on OT4 Passport
        """

        return Response(
            status=status.HTTP_200_OK,
            data={"service_key": settings.PASSPORT_SERVICE_KEY},
        )


class ServiceLoginViewSet(GenericViewSet):
    authentication_classes = [PassportAuthBackendMainEndpoint]

    @swagger_auto_schema(
        responses={204: serializers.Serializer()},
    )
    @action(detail=False, methods=["get"])
    def check_access_token(self, request):
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def profile_social_connections(self, request):
        """
        Made server-server request for get profile social connections by login
        """
        passport_response = PassportProxy.profile_social_connections(request)
        return Response(
            data=passport_response.json(),
            status=passport_response.status_code,
        )


class UpdateUserInfoViewSet(GenericViewSet):
    serializer_class = UpdateUserInfoSerializer
    permission_classes = [AllowAny]

    @action(
        detail=False,
        methods=["post"],
        serializer_class=UpdateUserInfoSerializer,
    )
    def email(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.data)
        old_email = data.get("old_email")
        new_email = data.get("new_email")

        if not new_email:
            raise ValidationError("New email can't be empty")

        try:
            user = User.objects.get(email__iexact=old_email)
            user.email = new_email
            user.is_email_verified = data.get("is_email_verified")
            user.extra["email_change_to"] = ""
            user.save()

            # add logs
            loguru.logger.info(
                f"User {user.id} update email from {old_email} to {new_email}"
            )
        except User.DoesNotExist:
            raise ValidationError(f"User with email {old_email} does not exist.")
        except User.MultipleObjectsReturned:
            raise ValidationError(f"Returned more than one User with email {old_email}")

        # Call update user hook
        on_update_user(user.id)

        return Response(status=status.HTTP_200_OK)
