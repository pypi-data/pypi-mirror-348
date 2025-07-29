from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db.models.functions import Lower
from loguru import logger


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("start to lowercase")

        User_model = get_user_model()
        User_model.objects.update(email=Lower('email'))

        logger.info("Db emails was update")
