from urllib.parse import urlencode

import httpx
from django.conf import settings


class AbstractPassportProxy:
    """
    Class for managing passport proxy.
    """
    # в методах исправить параметры - сделать такие же, как и в классе ниже
    @classmethod
    def profile_social_connections(cls, request):
        """
        Made server-server request for get profile social connections by login
        """
        raise NotImplementedError

    @classmethod
    def change_mobile(cls, request):
        """
        Made server-server request for change mobile
        """
        raise NotImplementedError

    @classmethod
    def confirm_mobile(cls, request):
        """
        Made server-server request for confirm change mobile
        """
        raise NotImplementedError

    @classmethod
    def is_unique(cls, request):
        """
        Made server-server request for check unique fields
        """
        raise NotImplementedError

    @classmethod
    def login(cls,request):
        """
        Made server-server request for login
        """
        raise NotImplementedError

    @classmethod
    def registration(cls, request):
        """
        Made server-server request for registration
        """
        raise NotImplementedError

    @classmethod
    def continue_login(cls, request):
        """
        Made server-server request for continue flow
        """
        raise NotImplementedError

    @classmethod
    def password_reset(cls, request):
        """
        Made server-server request for profile password reset
        """
        raise NotImplementedError

    @classmethod
    def change_password(cls, request):
        """
        Made server-server request for change password
        """
        raise NotImplementedError

    @classmethod
    def connections_list(cls, request):
        """
        Made server-server request for get connections list
        """
        raise NotImplementedError


class PassportProxy(AbstractPassportProxy):
    """
    Default passport proxy methods
    """
    @classmethod
    def profile_social_connections(cls, request):
        response = httpx.post(
            settings.PASSPORT_PROFILE_SOCIAL_CONNECTIONS_URL,
            json=request.data,
            timeout=120,
        )
        return response

    @classmethod
    def change_mobile(cls, request):
        response = httpx.post(
            settings.PASSPORT_CHANGE_PHONE_URL,
            json=request.data,
            headers={"Authorization": request.headers["Authorization"]},
            timeout=120,
        )
        return response

    @classmethod
    def confirm_mobile(cls, request):
        response = httpx.post(
            settings.PASSPORT_CONFIRM_CHANGE_PHONE_URL,
            json=request.data,
            headers={"Authorization": request.headers["Authorization"]},
            timeout=120,
        )
        return response

    @classmethod
    def is_unique(cls, request):
        response = httpx.post(settings.PASSPORT_IS_UNIQUE_URL, json=request.data, timeout=120)
        return response

    @classmethod
    def login(cls, request):

        data = dict(
            login=request.data.get("login"),
            password=request.data.get("password")
        )

        query_params = {**request.query_params, "service_key": settings.PASSPORT_SERVICE_KEY}
        login_url = f"{settings.PASSPORT_API_LOGIN_URL}?{urlencode(query_params)}"

        response = httpx.post(login_url, json=data, timeout=120)

        return response

    @classmethod
    def registration(cls, request):
        """
        Server-server passport registration
        """
        data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password": request.data.get("password"),
            "password2": request.data.get("password2"),
        }

        query_params = {**request.query_params, "service_key": settings.PASSPORT_SERVICE_KEY}
        registration_url = f"{settings.PASSPORT_API_REGISTRATION_URL}?{urlencode(query_params)}"

        response = httpx.post(registration_url, json=data, timeout=120)

        return response

    @classmethod
    def continue_login(cls, request):
        query_params = request.GET.urlencode()
        continue_url = f"{settings.PASSPORT_CONTINUE_URL}?{query_params}"
        response = httpx.post(
            continue_url,
            headers={"Authorization": request.headers["Authorization"]},
            timeout=300,
        )
        return response

    @classmethod
    def password_reset(cls, request):
        response = httpx.post(
            url=settings.PASSPORT_PASSWORD_RESET_URL,
            json=request.data,
            timeout=300,
        )
        return response

    @classmethod
    def change_password(cls, request):
        response = httpx.put(
            url=settings.PASSPORT_CHANGE_PASSWORD_URL,
            json=request.data,
            headers={"Authorization": request.headers["Authorization"]},
            timeout=300,
        )
        return response

    @classmethod
    def change_password_v2(cls, request):
        response = httpx.put(
            url=settings.PASSPORT_CHANGE_PASSWORD_V2_URL,
            json=request.data,
            headers={"Authorization": request.headers["Authorization"]},
            timeout=300,
        )
        return response

    @classmethod
    def connections_list(cls, request):
        response = httpx.get(
            url=settings.PASSPORT_CONNECTIONS_LIST_URL,
            headers={"Authorization": request.headers["Authorization"]},
            timeout=120,
        )
        return response
