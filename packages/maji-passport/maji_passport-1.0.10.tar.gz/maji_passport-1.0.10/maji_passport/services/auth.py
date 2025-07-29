import datetime
import random

import jwt
import sentry_sdk
from countries_plus.models import Country
from django.contrib.auth import get_user_model
from django.core.exceptions import (
    ObjectDoesNotExist,
    PermissionDenied,
    MultipleObjectsReturned,
)
from django.db import IntegrityError, transaction
from django.conf import settings
from django.utils import timezone
from jwt import InvalidAlgorithmError, ExpiredSignatureError, InvalidSignatureError
from loguru import logger

from maji_passport.models import PassportUser, AccessToken, TargetAccess, BlackListToken
from maji_passport.services.exchange import ExchangeTokenService

User = get_user_model()


class RSAManager:
    _instance = None
    file_data = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RSAManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def read_file(self, file_path):
        with open(file_path, "r") as file:
            self.file_data = file.read()

    def get_file_data(self):
        return self.file_data


rsa_manager = RSAManager()
rsa_manager.read_file(settings.PASSPORT_PUBLIC_KEY_PATH)


class RSAPassportService:
    def __init__(
        self,
        iat,
        exp,
        user_uuid,
        country_iso,
        access_token,
        target_access=TargetAccess.MAIN.value,
        # deprecated
        user_auth_code="",
        email="",
        username="",
    ):
        self.passport_uuid = user_uuid
        self.country_iso = country_iso
        self.access_token = access_token
        self.iat = iat
        self.exp = exp

    def _create_user(self):
        try:
            with transaction.atomic():
                country = Country.objects.get(iso=self.country_iso)
                user = User.objects.create(
                    uuid=self.passport_uuid,
                    email=f"email-{random.randint(0000000, 9999999)}@random.ra",
                    username=f"user-{random.randint(0000000, 9999999)}",
                    country_on_create=country,
                )
                user.register_and_save()
                user.extra["migrated_to_passport"] = True
                user.save()
        except IntegrityError as e:
            if ("users_uuid" or "user_uuid") in e.args[0]:
                return User.objects.get(uuid=self.passport_uuid)
            if "duplicate key" in e.args[0]:
                user = self._create_user()
            else:
                raise e
        return user

    def _preprocess_prepare_passport(self):
        passport_query = PassportUser.objects.filter(passport_uuid=self.passport_uuid)
        if passport_query.exists():
            passport = passport_query.first()
            error_message = f"RSAPassportService._preprocess_prepare_passport: {self.passport_uuid} - not uniq"
            logger.warning(error_message)
            sentry_sdk.capture_message(error_message)
            return passport, False

        else:
            passport = PassportUser.objects.create(
                passport_uuid=self.passport_uuid,
                user_auth_code="",
            )
            try:
                # check if user with uuid=passport_uuid exists, we return second param False
                user = User.objects.get(uuid=self.passport_uuid)
                passport.argo_user = user
                passport.save()

                logger.info(
                    f"User with passport_uuid={self.passport_uuid} already exists "
                    f"and add to created passport"
                )

                return passport, False
            except ObjectDoesNotExist:
                return passport, True

    def _prepare_passport(self, user) -> PassportUser:
        passport, created = PassportUser.objects.get_or_create(
            argo_user_id=user.id,
            defaults={
                "user_auth_code": "",
                "passport_uuid": self.passport_uuid,
            },
        )
        return passport

    def _prepare_access_token(self, passport: PassportUser) -> AccessToken:
        try:
            access_token_obj = AccessToken.objects.get(
                passport_user=passport, target=TargetAccess.MAIN
            )
            access_token_obj.token = self.access_token
            access_token_obj.token_expiration = datetime.datetime.utcfromtimestamp(
                self.exp
            )
            access_token_obj.save()
        except ObjectDoesNotExist:
            access_token_obj = AccessToken.objects.create(
                passport_user=passport,
                target=TargetAccess.MAIN,
                token=self.access_token,
                token_expiration=datetime.datetime.utcfromtimestamp(self.exp),
            )
            logger.info(
                f"Create AccessToken object for " f"the user {passport.passport_uuid}"
            )
        except MultipleObjectsReturned:
            access_token_obj = AccessToken.objects.filter(
                passport_user=passport, target=TargetAccess.MAIN
            ).last()
            access_token_obj.token = self.access_token
            access_token_obj.token_expiration = datetime.datetime.utcfromtimestamp(
                self.exp
            )
            access_token_obj.save()
            logger.warning(
                f"AccessToken MultipleObjectsReturned for "
                f"the user {passport.passport_uuid}"
            )
        return access_token_obj

    def prepare_user(self, for_kafka=False):
        new_user = False
        try:
            with transaction.atomic():
                passport = PassportUser.objects.get(passport_uuid=self.passport_uuid)
                user = passport.argo_user
                if not user:
                    raise ObjectDoesNotExist
        except MultipleObjectsReturned:
            last_object = PassportUser.objects.filter(
                passport_uuid=self.passport_uuid
            ).last()
            if last_object:
                last_object.delete()

            passport = PassportUser.objects.get(passport_uuid=self.passport_uuid)
            user = passport.argo_user

        except ObjectDoesNotExist:
            passport, new_user = self._preprocess_prepare_passport()

            if new_user or not passport.argo_user:
                new_user = True
                user = self._create_user()
                passport.argo_user = user
                passport.save()
                logger.info(
                    f"User with uuid doesn't exist: {self.passport_uuid}, "
                    f"created new - {user.uuid}"
                )
            else:
                user = passport.argo_user

        logger.info(f"Get passport for passport_uuid {self.passport_uuid}")
        access_token_obj = None
        if not for_kafka:
            # Saving new access token
            # Segment avoiding if execution is from SyncService(for_kafka)
            access_token_obj = self._prepare_access_token(passport)

        if for_kafka or (
            new_user
            and getattr(settings, "PASSPORT_KAFKA_UPDATE", None)
            and self.access_token
        ):
            # todo think about async server-server, without waiting response. Possible error
            data = {"uuid": self.passport_uuid}
            url = settings.PASSPORT_KAFKA_UPDATE
            if for_kafka:
                # if the request is from SyncService,
                # we have to execute it without access_token.
                # We use another endpoint with secret key
                data["key"] = settings.PASSPORT_KAFKA_UPDATE_KEY
                url = settings.PASSPORT_KAFKA_UPDATE_BY_KEY_URL

            ExchangeTokenService.send_post_request(
                url,
                data,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )

        return user, access_token_obj

    @staticmethod
    def parse_token(token) -> dict:
        rsa_manager = RSAManager()
        public_key = rsa_manager.get_file_data()
        try:
            decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        except InvalidAlgorithmError as e:
            logger.warning(f"Can't decode token: {token}")
            raise InvalidAlgorithmError(e)
        except ExpiredSignatureError as e:
            raise ExpiredSignatureError(e)
        except InvalidSignatureError as e:
            raise PermissionDenied(e)

        return decoded

    @staticmethod
    def create_token(passport, token, target, exp) -> AccessToken:
        access_token_obj = AccessToken.objects.create(
            passport_user=passport,
            target=target,
            token=token,
            token_expiration=exp,
        )
        return access_token_obj

    @staticmethod
    def clear_periodic_access_token():
        AccessToken.objects.filter(
            token_expiration__lt=timezone.now() - datetime.timedelta(days=180)
        ).delete()
        logger.info("Delete 180 days old AccessToken objects")

    @staticmethod
    def update_access_token(new_token):
        """
        Update passport user access token in service
        """
        payload = RSAPassportService.parse_token(new_token)
        service = RSAPassportService(**payload, access_token=new_token)
        passport, created = service._preprocess_prepare_passport()
        service._prepare_access_token(passport)


class BlackListService:
    @staticmethod
    def clear_periodic_blacklist():
        BlackListToken.objects.filter(
            token_expiration__lt=timezone.now() - datetime.timedelta(days=60)
        ).delete()
        logger.info("Delete 60 days old BlackListToken objects")
