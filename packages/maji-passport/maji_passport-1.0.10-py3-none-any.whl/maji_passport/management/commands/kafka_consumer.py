import os
import sys

from django.core.management.base import BaseCommand

from maji_passport.services.kafka import KafkaService


class Command(BaseCommand):
    help = "Run Kafka consumer"

    def handle(self, *args, **options):
        """
        Set up running consumer on Passport side
        """
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

        service = KafkaService()
        service.consume_messages()
