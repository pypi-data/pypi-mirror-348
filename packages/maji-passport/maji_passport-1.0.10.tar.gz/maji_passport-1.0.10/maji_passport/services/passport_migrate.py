import operator
from typing import List

import httpx
import loguru
import sentry_sdk
from django.conf import settings
from django.contrib.auth import get_user_model
from httpx import Response
from rest_framework import status

User = get_user_model()


class PassportMigrateService:
    """
    Service for migrate users to passport
    """

    @staticmethod
    def send_users_data(data_list: List[dict]):
        """
        Create requests to create user profiles in passport
        """

        split_list = [data_list[i : i + 1000] for i in range(0, len(data_list), 1000)]

        # migrate users info to passport
        for items in split_list:
            try:
                data = dict(users=items, key=settings.PASSPORT_SERVICE_KEY)
                response = httpx.post(
                    settings.PASSPORT_START_MIGRATE, json=data, timeout=120
                )

                if response.status_code != status.HTTP_200_OK:
                    sentry_sdk.capture_message(f"Users migrate: {response.json()}")
                    loguru.logger.error(f"Users migrate: {response.json()}")
                else:
                    # save in users what they migrated in passport
                    emails = list(map(operator.itemgetter("email"), items))
                    users = User.objects.filter(email__in=emails)
                    for user in users:
                        user.extra["migrated_to_passport"] = True

                    User.objects.bulk_update(users, fields=["extra"])

            except TimeoutError:
                loguru.logger.error(f"Users migrate: Timeout for request.")
                continue

    @staticmethod
    def migrate_password(email, password):
        """
        Migrate this user password to passport profile, if profile has not password
        """
        user = User.objects.filter(email=email).first()

        # if user password_migrated_to_passport is True we don't set password
        # to passport profile and return 304 not modified
        if user.extra.get("password_migrated_to_passport", False):
            response = Response(
                json={"password": "Password already migrated."},
                status_code=200,
            )
            return response

        data = dict(email=email, password=password, key=settings.PASSPORT_SERVICE_KEY)
        response = httpx.post(settings.PASSPORT_SET_PASSWORD, json=data, timeout=120)

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            sentry_sdk.capture_message(f"User password migrate: {response.json()}")
            loguru.logger.error(f"User password migrate: {response.json()}")

        # if we have not errors from passport service
        # we save user extra "password_migrated_to_passport" is True
        user.extra["password_migrated_to_passport"] = True
        user.save()

        return response
