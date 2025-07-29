import json
import os
import sys

from django.core.management.base import BaseCommand

from maji_passport.services.kafka import KafkaService


class Command(BaseCommand):
    help = "Execute test command to produce message to consumer"

    def handle(self, *args, **options):
        """
        Command for test run producer. This part must be on internal service side
        """
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

        service = KafkaService()
        message = {
            "action": "update_user_info",
            "uuid": "5dbbc798-c8f4-42ab-8682-ed0970a0140f",
            "description": "",
            "extra": {
                "email": "sasha.palant+293@gmail.com",
                "username": "pa293",
                "is_email_verified": False,
                "phone": "",
                "is_phone_verified": False,
                "user_data": {},
            },
        }
        service.produce_message(json.dumps(message))
