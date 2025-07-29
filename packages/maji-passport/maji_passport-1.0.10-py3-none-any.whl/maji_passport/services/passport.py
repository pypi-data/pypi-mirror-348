import datetime
from enum import Enum
from typing import List
from urllib.parse import urlencode
from venv import logger

import httpx
import loguru
import sentry_sdk
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError

from maji_passport.models import PassportUser
from maji_passport.services.auth import RSAPassportService
from maji_passport.services.exchange import ExchangeTokenService

User = get_user_model()


def has_passport(user: User) -> bool:
    """
    OneToOne specific.... Check if we have passport_user object for user
    """
    return hasattr(user, "passport_user") and user.passport_user


class PassportService:
    class UserSyncStatus(Enum):
        MATCHED = "matched"
        REGISTERED = "registered"

    def __init__(self, passport: PassportUser):
        self.passport = passport

    def invalidate_access_tokens(self) -> None:
        self.passport.accesstoken_set.update(token_expiration=datetime.datetime.now())

    @classmethod
    def update_passport_token(cls, token: str):
        params = {
            "service_key": settings.PASSPORT_SERVICE_KEY,
        }

        response_dict = ExchangeTokenService.send_post_request(
            settings.PASSPORT_UPDATE_TOKEN_URL + "?" + urlencode(params),
            {},
            headers={"Authorization": f"Bearer {token}"},
        )
        new_token = response_dict.get("access_token")

        # update token
        # url = f"https://{settings.CONSOLE_DOMAIN}/api/auth/user/"
        # httpx.get(
        #     url,
        #     headers={"Authorization": f"Bearer {new_token}"},
        #     timeout=120,
        # )
        # TODO: в комьюнити для апдейта токена используется следующее
        #  и не дергается /api/auth/user. Нужно будет на арго/брендоне тоже
        #  удалить вызов /api/auth/user проверить это
        # # update token in this service
        RSAPassportService.update_access_token(new_token)
        return new_token

    @classmethod
    def send_data_to_passport(cls, passport_user: PassportUser, data: dict):
        """
        Prepare and send main data and other user_data to passport.
        """

        access_token = passport_user.accesstoken_set.filter(target="main").last()
        token = access_token.token

        # pop types and description bcs PassportUser model has not this fields now
        data.pop("types", None)
        data.pop("description", None)

        # pop main data, bcs other data we send to another endpoint
        main_data = {}
        username = data.pop("username", None)
        email = data.pop("email", None)

        if username:
            main_data["username"] = username
        if email:
            main_data["email"] = email

        main_data_url = settings.PASSPORT_PROFILE_UPDATE_URL
        main_data_url_dict = dict(
            url=main_data_url,
            json=main_data,
            headers={"Authorization": f"Bearer {token}"},
            timeout=300,
        )

        # send main data update
        response_main_data = httpx.patch(**main_data_url_dict)

        # if token is expired we update token and resend data
        if response_main_data.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]:
            token = PassportService.update_passport_token(token)
            main_data_url_dict["headers"] = {"Authorization": f"Bearer {token}"} # request with new token
            response_main_data = httpx.patch(**main_data_url_dict)

        if response_main_data.status_code != status.HTTP_200_OK:
            logger.warning(f"Passport main data update error: {response_main_data.json()}, {data}")
            raise ValidationError(response_main_data.json(), code=response_main_data.status_code)

        # update user_data
        user_data_url = settings.PASSPORT_USERDATA_UPDATE_URL
        response_user_data = httpx.patch(
            url=user_data_url,
            json=data,
            headers={"Authorization": f"Bearer {token}"},
            timeout=300,
        )
        if response_user_data.status_code != status.HTTP_200_OK:
            logger.warning(f"Passport userdata update error: {response_user_data.json()}, {data}")
            raise ValidationError(response_user_data.json(), code=response_user_data.status_code)

        # update PassportUser in service instantly
        PassportUser.objects.filter(passport_uuid=passport_user.passport_uuid).update(**data)

    @classmethod
    def passport_registration(cls, username: str, email: str, password: str):
        """
        Server-server passport registration
        """
        data = {
            "username": username,
            "email": email,
            "password": password,
            "password2": password,
        }

        response = httpx.post(settings.PASSPORT_API_REGISTRATION_URL, json=data, timeout=120)
        if response.status_code != status.HTTP_201_CREATED:
            logger.error(f"Passport registration failed with code {response.status_code}. "
                         f"Response: {response.json()}. "
                         f"Data: {data}.")
            raise ValidationError(response.json())

    @classmethod
    def match_passport_profile(self, email: str) -> str:
        """
        Server-server matching user email with maji-passport in this service.
        If match is success - return profile uuid
        """

        # check if email already exists in passport
        unique_email_response = httpx.post(settings.PASSPORT_IS_UNIQUE_URL, json=dict(email=email), timeout=120)
        is_unique_email = unique_email_response.json().get("email", False)
        logger.info(f"Match passport: {is_unique_email=}")
        # if email is unique, that mean we maji has not profile with that email
        if is_unique_email:
            return ""

        logger.info(f"Start matching user with email {email} in this service")
        data = {
            "email": email,
            "service_key": settings.PASSPORT_SERVICE_KEY,
            "exchange_key": settings.PASSPORT_EXCHANGE_KEY,
        }
        response = httpx.post(settings.PASSPORT_MATCH_PROFILE_URL, json=data, timeout=120)
        if response.status_code != status.HTTP_200_OK:
            sentry_sdk.capture_message(f"Users migrate: {response.json()}")
            loguru.logger.error(f"Matching passport error: {response.json()}")

        return response.json().get("uuid")

    @classmethod
    def match_or_register_passport(cls, username: str, email: str, password: str) -> UserSyncStatus:
        """
        Server-server match or register passport for user
        """
        passport_uuid = PassportService.match_passport_profile(email)
        logger.info(f"Match passport: {passport_uuid=}")
        if not passport_uuid:
            PassportService.passport_registration(username, email, password)
            # login in passport for create PassportUser in service
            PassportService.passport_login(email, password)
            return PassportService.UserSyncStatus.REGISTERED
        return PassportService.UserSyncStatus.MATCHED

    @classmethod
    def passport_login(cls, login: str, password: str):
        """
        Login in passport and return token
        Create PassportUser in service if user has not it
        """
        data = dict(login=login, password=password, service_key=settings.PASSPORT_SERVICE_KEY)
        passport_response = httpx.post(
            settings.PASSPORT_API_LOGIN_URL, json=data, timeout=120
        )

        if passport_response.status_code == status.HTTP_200_OK:
            token = passport_response.json()["access_token"]
            user = User.objects.filter(Q(username__iexact=login) | Q(email__iexact=login)).first()

            if not PassportUser.objects.filter(argo_user=user).exists():
                # if not PassportUser for this user we need create it in service
                payload = RSAPassportService.parse_token(token)
                service = RSAPassportService(**payload, access_token=token)
                passport, created = service._preprocess_prepare_passport()

                passport.argo_user = user
                passport.save()

                # create AccessToken object for this passport
                service._prepare_access_token(passport)
            return token, user
        else:
            raise ValidationError(passport_response.json())

    # TODO: DEPRECATED??
    @classmethod
    def clean_up_passport(cls, passport_user: PassportUser):
        data = {
            "uuid": str(passport_user.passport_uuid),
            "exchange_key": settings.PASSPORT_EXCHANGE_KEY,
        }
        response = httpx.post(
            settings.PASSPORT_CLEAN_UP_URL,
            json=data,
            timeout=120
        )
        if response.status_code != status.HTTP_200_OK:
            logger.error(f"Passport can't delete profile: "
                         f"{response.json()}, uuid: {str(passport_user.passport_uuid)}")
            raise ValidationError(response.json(), code=response.status_code)
        logger.info(f"Clean up passport: {str(passport_user.passport_uuid)} success")

    @staticmethod
    def get_user(user_uuid: str) -> PassportUser:
        target_user = (
            PassportUser.objects.filter(passport_uuid=user_uuid)
            .prefetch_related("argo_user")
            .first()
        )
        if not target_user:
            raise ValidationError(code=404, detail="User not found.")
        return target_user

    @staticmethod
    def get_users(user_uuid_list: List[str]) -> List[PassportUser]:
        users = (
            PassportUser.objects.filter(passport_uuid__in=user_uuid_list)
            .prefetch_related("argo_user")
            .all()
        )
        return users


class PassportUserDataService:
    """
    Service for get user data from passport
    """
    @classmethod
    def get_social_link(cls, obj, platform):
        """
        Params:
            obj - User or PassportUser object
            platform - social network platform name: facebook, tiktok, etc.
        """
        social_username = obj.social_networks.get(platform, None)
        if social_username:
            social_link = f"{settings.SOCIAL_PLATFORMS.get(platform)}{social_username}"
            return social_link
        return None

    @classmethod
    def get_avatar_url(cls, user: User) -> str:
        if not user:
            return None
        if has_passport(user) and user.passport_user.avatar_url:
            return user.passport_user.avatar_url
        elif user.avatar:
            return user.avatar.original.url
        elif user.random_avatar:
            return user.random_avatar.original.url
        else:
            return None

    @classmethod
    def get_cover_url(cls, user: User) -> str:
        if not user:
            return None
        if has_passport(user) and user.passport_user.cover_url:
            return user.passport_user.cover_url
        if user.cover:
            return user.cover.original.url
        return None

    @classmethod
    def get_display_name(cls, user: User) -> str:
        if not user:
            return None
        if has_passport(user) and user.passport_user.display_name:
            return user.passport_user.display_name
        if user.display_name:
            return user.display_name
        return None

    @classmethod
    def get_social_links(cls, user: User) -> dict:
        """
        Return full social network url for object
        """
        if not user:
            return None

        social_links = {}

        if has_passport(user) and user.passport_user.social_networks:
            for platform in user.passport_user.social_networks:
                social_links[platform] = PassportUserDataService.get_social_link(
                    user.passport_user,
                    platform,
                )
            return social_links

        user_social_networks = user.social_networks
        if user_social_networks:
            for platform in user_social_networks:
                social_links[platform] = PassportUserDataService.get_social_link(
                    user,
                    platform,
                )
            return social_links
        return None

    @classmethod
    def get_social_networks(cls, user: User) -> dict:
        """
        Return social networks usernames
        """
        if not user:
            return None
        if has_passport(user) and user.passport_user.social_networks:
            return user.passport_user.social_networks
        if user.social_networks:
            return user.social_networks
        return None
