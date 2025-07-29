import argparse

import httpx
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from loguru import logger

User = get_user_model()

class Command(BaseCommand):
    """
    Command for check random users and trying to update them

    Default only log lists for update, with argument "--run" it will update "one_user_random" list
    """
    def add_arguments(self, parser):
        parser.add_argument("--run", dest="run", action=argparse.BooleanOptionalAction)

    def handle(self, *args, **options):
        run_check = options.get("run", False)
        logger.info("start check users")
        users_without_passports = []
        one_user_random = []

        users = User.objects.filter(email__contains="@random.ra").all()
        for user in users:
            if not hasattr(user, "passport_user"):
                logger.warning(f"user {user} doesn't have passport")
                users_without_passports.append(user)
                continue
            passport = user.passport_user
            logger.warning(f"user {user} has passport, but doesn't have normal email or username. ")
            one_user_random.append(passport)

            if run_check:
                data = dict(key=settings.PASSPORT_KAFKA_UPDATE_KEY, uuid=str(passport.passport_uuid))
                response = httpx.post(settings.PASSPORT_KAFKA_UPDATE_BY_KEY_URL, json=data, timeout=120)
                if response.status_code > 300:
                    logger.error(f"kafka update error: {response.json()}")
                else:
                    logger.warning(f"User {passport.passport_uuid} pushed to updated")



        logger.info(f"users_without_passports: {users_without_passports}")
        logger.info(f"one_user_random: {one_user_random}")

        logger.info("start check users")
