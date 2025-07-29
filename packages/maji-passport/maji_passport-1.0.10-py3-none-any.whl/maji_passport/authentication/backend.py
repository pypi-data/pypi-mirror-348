import datetime
import re
from typing import Iterable

from constance import config
from django.conf import settings
from jwt import InvalidAlgorithmError, ExpiredSignatureError, DecodeError
from loguru import logger
from rest_framework.exceptions import (
    AuthenticationFailed,
    PermissionDenied,
)

from maji_passport.models import AccessToken, BlackListToken
from maji_passport.services.auth import RSAPassportService
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

APPLICATION_AUTHENTICATION = (
    settings.INHERITANCE_AUTHENTICATION
    if getattr(settings, "APPLICATION_AUTHENTICATION")
    else JSONWebTokenAuthentication
)


class CommonPassportBackend(APPLICATION_AUTHENTICATION):
    def check_permission(self, access_token_obj):
        raise NotImplementedError

    def logg_all_request(self, request, user):
        if getattr(config, "LOG_ALL_REQUESTS", False):
            full_path = request.get_full_path()
            if isinstance(user, Iterable) and user[0]:
                user = user[0]
            logger.info(
                f"[ARGO-8723] User: {user}"
                f" called URI: {full_path}"
                f" with method: {request.method}"
            )

    def _authenticate_by_passport(self, request):
        """
        New authentication logic here
        Return the user object if authentication is successful, None otherwise"
        """
        token = request.headers.get("Authorization")
        if not token:
            return None, None
        token = re.sub(r"^Bearer\s*", "", token).strip()

        access_token_obj = AccessToken.objects.filter(token=token).last()
        if (
            access_token_obj
            and access_token_obj.passport_user
            and getattr(access_token_obj.passport_user, "argo_user", None)
        ):
            return self.check_permission(access_token_obj)
        else:
            try:
                payload = RSAPassportService.parse_token(token)

                # Check if the token was invalidated
                access_token_obj = BlackListToken.objects.filter(token=token).last()
                if access_token_obj:
                    raise PermissionDenied("Token is expired")

                service = RSAPassportService(**payload, access_token=token)
                return service.prepare_user()
            except InvalidAlgorithmError:
                # this error is thrown if user try to connect with old token and it will pass the user to django auth
                pass
            except ExpiredSignatureError:
                raise AuthenticationFailed("Token is expired")
            return None, None

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise, returns `None`.
        """

        user = self._authenticate_by_passport(request)
        if isinstance(user, Iterable) and user[0]:
            self.logg_all_request(request, user[0])
            return user

        try:
            user = super().authenticate(request)
        except AuthenticationFailed:
            logger.warning(
                f"Base auth. Invalid token. {request}, data: {request.data}, "
                f"meta: {request.META.get('HTTP_USER_AGENT', '')}, bearer: {request.headers['Authorization']}"
            )
            raise AuthenticationFailed
        self.logg_all_request(request, user)

        return user


class CommonPassportBackendWithoutCreateUser(CommonPassportBackend):
    def _authenticate_by_passport(self, request):
        """
        New authentication logic here
        Return the user object if authentication is successful, None otherwise"
        """

        token = request.headers.get("Authorization")
        if not token:
            return None, None
        token = re.sub(r"^Bearer\s*", "", token).strip()

        access_token_obj = AccessToken.objects.filter(token=token).last()
        if access_token_obj and access_token_obj.passport_user is not None:
            return self.check_permission(access_token_obj)
        else:
            return None, None


class PassportAuthPermission(APPLICATION_AUTHENTICATION):
    def check_permission(self, access_token_obj):
        if access_token_obj.is_token_expired:
            try:
                payload = RSAPassportService.parse_token(access_token_obj.token)
            except InvalidAlgorithmError or DecodeError:
                return None, None
            except ExpiredSignatureError:
                raise AuthenticationFailed("Token is expired")

            cert_exp = datetime.datetime.utcfromtimestamp(payload["exp"])
            if cert_exp < datetime.datetime.now():
                raise AuthenticationFailed("Token is expired")
            else:
                access_token_obj.token_expiration = cert_exp
                access_token_obj.save()
        return access_token_obj.passport_user.argo_user, access_token_obj.token


class PassportAuthPermissionWithoutCreate(APPLICATION_AUTHENTICATION):
    def check_permission(self, access_token_obj):
        if access_token_obj.is_token_expired:
            raise AuthenticationFailed("Token is expired")
        return access_token_obj.passport_user.argo_user, access_token_obj.token


class PassportAuthBackendMainEndpoint(PassportAuthPermission, CommonPassportBackend):
    """
    For passport auth with automatically creation users and passport
    """

    pass


class PassportAuthBackend(
    PassportAuthPermissionWithoutCreate, CommonPassportBackendWithoutCreateUser
):
    """
    Only for auth
    """

    pass


class PassportExpireTokenBackend(CommonPassportBackendWithoutCreateUser):
    """
    Update token for only seamless flow
    """

    def check_permission(self, access_token_obj):
        pass
