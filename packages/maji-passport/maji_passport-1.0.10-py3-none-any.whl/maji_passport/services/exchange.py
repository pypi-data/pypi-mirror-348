import re
from urllib.parse import urlencode

import httpx
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from loguru import logger
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from maji_passport.serializers.exchange import (
    TokenExchangeResponseSerializer,
    TokenExchangeCompleteSerializer,
    ExtraTokenRequestSerializer,
    AccessTokenSerializer,
)
from maji_passport.models import PassportUser, AccessToken, TargetAccess

User = get_user_model()


class ExchangeTokenService:
    def __init__(self, user_uuid, country_iso, user_auth_code="", email="", username=""):
        self.email = email
        self.passport_uuid = user_uuid
        self.user_auth_code = user_auth_code
        self.username = username
        self.country_iso = country_iso

    @staticmethod
    def send_post_request(url, data, headers=None) -> dict:
        if not headers:
            headers = {}
        logger.info(f"send_post_request: {url}, {data}")
        response = httpx.post(url, headers=headers, json=data, timeout=300)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return {}
        if response.status_code != status.HTTP_200_OK:
            logger.error(f"send_post_request {url} {data}")
            raise PermissionDenied("Exchange server-server token is invalid")
        output = response.json()
        logger.info(f"send_post_request.output: {output}")
        return output

    @staticmethod
    def request_for_extra_token(request, target:str = "") -> dict:
        """
        For android connect
        """
        token = re.sub(r"^Bearer\s*", "", request.headers['Authorization']).strip()
        params = {
            "service_key": settings.PASSPORT_SERVICE_KEY,
            "token_target": target,
        }

        response_dict = ExchangeTokenService.send_post_request(
            settings.PASSPORT_EXTRA_TOKEN_URL + "?" + urlencode(params),
            params,
            headers={"Authorization": f"Bearer {token}"},
        )
        serializer = AccessTokenSerializer(data=response_dict)
        serializer.is_valid(raise_exception=True)
        return serializer.data
