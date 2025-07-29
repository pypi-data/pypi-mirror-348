import datetime
import time
from urllib.parse import urlencode

import httpx
import sentry_sdk
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from loguru import logger
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from maji_passport.models import PassportUser
from maji_passport.serializers.passport import (
    UserPassportSetPasswordSerializer,
    GetLoginUrlOutputSerializer,
    UserPassportUpdateSerializer,
)
from maji_passport.services.passport_migrate import PassportMigrateService
from maji_passport.utils import invalidate_cache, format_cache_prefix

User = get_user_model()


class UserPassportViewSet(GenericViewSet):
    queryset = User.objects.all()

    @action(
        detail=False,
        methods=["PATCH"],
        serializer_class=UserPassportUpdateSerializer,
    )
    def user(self, request):
        """
        Handle for update PassportUser
        """
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, request.data)

        cache_key = format_cache_prefix(
            settings.AUTH_USER_API_CACHE, request.user.id
        )
        invalidate_cache(cache_key)

        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["POST"],
        serializer_class=UserPassportSetPasswordSerializer,
    )
    def migrate_password(self, request):
        """
        Migrate user password to passport profile
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        passport_response = PassportMigrateService.migrate_password(
            email=user.email,
            password=serializer.data["password"],
        )

        return Response(passport_response.json(), status=passport_response.status_code)

    @swagger_auto_schema(
        request_body=Serializer,
        responses={204: Serializer()},
    )
    @action(
        detail=False,
        methods=["POST"],
    )
    def set_tokens_expired(self, request):
        """
        Expired user token
        """

        access_token = request.user.passportuser.accesstoken_set.filter(
            target="main"
        ).first()
        access_token.token_expiration = timezone.now() - datetime.timedelta(hours=10)
        access_token.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PassportViewSet(GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = GetLoginUrlOutputSerializer

    @action(
        detail=False,
        methods=["GET"],
    )
    def get_login_url(self, request):
        """
        Get url for passport login
        """
        params = {
            "service_key": settings.PASSPORT_SERVICE_KEY,
        }
        backwards_url = request.GET.get("backwards_url", None)
        if backwards_url:
            params["backwards_url"] = backwards_url

        serializer = self.serializer_class(
            {"url": settings.PASSPORT_LOGIN_URL + "?" + urlencode(params)}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteUserView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Made server-server request for clean up user.
        """
        if request.data["exchange_key"] != settings.PASSPORT_EXCHANGE_KEY:
            raise ValidationError("Wrong exchange_key")

        passport_uuid = request.data["passport_uuid"]
        try:
            passport_user = PassportUser.objects.get(passport_uuid=passport_uuid)

            # start clean up process and clean up user
            argo_user = passport_user.argo_user
            argo_user.start_delete_process()
            argo_user.clear_user_data()

            # delete status for send to passport
            delete_status = "DELETED"

        except ObjectDoesNotExist:
            sentry_sdk.capture_message(f"DeleteConfirm for maji-passport WARNING: "
                                       f"Passport user with uuid {passport_uuid} does not exist")
            logger.warning(f"DeleteConfirm for maji-passport WARNING: "
                           f"Passport user with uuid {passport_uuid} does not exist")
            # delete status for send to passport
            delete_status = "NOT DELETED"
        except Exception as e:
            sentry_sdk.capture_message(f"DeleteConfirm for maji-passport WARNING: {e}")
            logger.warning(f"DeleteConfirm for maji-passport WARNING: {e}")
            # delete status for send to passport
            delete_status = "NOT DELETED"

        # send to passport signal what user already cleared
        delete_confirm_url = settings.PASSPORT_CONFIRM_DELETE_URL
        if getattr(settings, "BRANDON", None):
            platform = "brandon"
        elif getattr(settings, "COMMUNITY", None):
            platform = "community"
        else:
            platform = "argo"

        confirm_data = {
            "exchange_key": settings.PASSPORT_EXCHANGE_KEY,
            "uuid": passport_uuid,
            "platform": platform,
            "status": delete_status,
        }

        response = httpx.post(delete_confirm_url, json=confirm_data, timeout=300)
        if response.status_code != status.HTTP_200_OK:
            sentry_sdk.capture_message(f"DeleteConfirm Failed for {passport_uuid}: {response.json()}")
            logger.error(f"DeleteConfirm Failed for {passport_uuid}: {response.json()}")

        return Response(status=response.status_code)