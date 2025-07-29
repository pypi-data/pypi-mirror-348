import argparse

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from loguru import logger

from maji_passport.models import PassportUser

User = get_user_model()

class Command(BaseCommand):
    """
    Command for delete duplicates users and passports
    Finding not completed users, check their passports
    Finding duplicates, check the subscriptions on duplicated
    Deleted not completed users

    Default only log lists for delete, with argument "--run" it will delete "passports_to_delete" list
    """
    def add_arguments(self, parser):
        parser.add_argument("--run", dest="run", action=argparse.BooleanOptionalAction)

    def handle(self, *args, **options):
        run_delete = options.get("run", False)
        logger.info("start delete duplicate")
        users_without_passports = []
        one_user_random = []
        impossible_to_delete = []
        SubscriptionModel = apps.get_model("subscription", "Subscription")
        RokuUserModel = apps.get_model("users", "RokuUser")
        users = User.objects.filter(email__contains="@random.ra").all()
        for user in users:
            if not hasattr(user, "passport_user"):
                logger.warning(f"user {user} doesn't have passport")
                users_without_passports.append(user)
                continue
            passport = user.passport_user
            count = PassportUser.objects.filter(passport_uuid=str(passport.passport_uuid)).count()
            if count == 1:
                logger.warning(f"user {user} has passport, but doesn't have normal email or username. "
                               f"Possibly Roku user, where we can't change name because of already used username. "
                               f"Or other validation error on Kafka")
                one_user_random.append(user)
            else:
                passports = PassportUser.objects.filter(passport_uuid=str(passport.passport_uuid))
                passports_to_delete = []
                for el in passports:
                    if "@random.ra" in el.argo_user.email:
                        if SubscriptionModel.objects.filter(user=el.argo_user).exists():
                            logger.error(f"User {user} has subscriptions. Impossible to delete")
                            impossible_to_delete.append(user)
                            continue
                        if RokuUserModel.objects.filter(user=el.argo_user).exists():
                            logger.error(f"User {user} has subscriptions. Impossible to delete")
                            impossible_to_delete.append(user)
                            continue

                        passports_to_delete.append(el)
                        logger.info(f"Prepare user {el} to delete")
                    else:
                        logger.info(f"for uuid {passport.passport_uuid} - user {el} is main. No further actions")
                        continue

                if passports.count() == len(passports_to_delete):
                    logger.error(f"All users {passports_to_delete} are not completed. Impossible to delete")
                    impossible_to_delete.extend(passports_to_delete)
                    continue

                logger.warning(f"Users {passports_to_delete} will be delete")
                if run_delete:
                    for el in passports_to_delete:
                        user = el.argo_user # Delete all related ArgoUser objects
                        user.clear_user_data()
                        user.extra["passport_uuid"] = str(el.passport_uuid)
                        user.save()
                        el.delete()  # Delete the PassportUser


        logger.info(f"users_without_passports: {users_without_passports}")
        logger.info(f"one_user_random: {one_user_random}")
        logger.info(f"impossible_to_delete: {impossible_to_delete}")

        logger.info("end delete duplicate")
