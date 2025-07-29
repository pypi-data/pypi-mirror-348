import datetime
from enum import Enum
import json
from typing import List

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string
from loguru import logger

from confluent_kafka import Consumer, Producer, KafkaException
from django.utils.module_loading import import_string

from maji_passport.hooks import on_update_user
from maji_passport.models import PassportUser, BlackListToken, AccessToken
from maji_passport.services.passport import PassportService
from maji_passport.utils import invalidate_cache, format_cache_prefix

from maji_passport.serializers.kafka import KafkaUpdateUserSerializer

User = get_user_model()

class PassportKafkaService:
    @staticmethod
    def process_message(data):
        try:
            action_service = MessageActionService(**data)
        except TypeError as e:
            logger.error(e)
            return
        action = data.get("action", None)
        if action == MessageActionService.Action.LOGOUT.value:
            action_service.logout()
        elif action == MessageActionService.Action.UPDATE_USER_INFO.value:
            action_service.update_user()
        elif action == MessageActionService.Action.BLACK_LIST_TOKEN.value:
            action_service.add_to_black_list()
        elif action == MessageActionService.Action.START_CLEAN_UP_USER.value:
            action_service.start_clean_up_user()
        elif action == MessageActionService.Action.CANCEL_CLEAN_UP_USER.value:
            action_service.cancel_clean_up_user()
        elif action == MessageActionService.Action.CLEAN_UP_USER.value:
            action_service.clean_up_user()
        else:
            logger.warning("Unhandled action")



class KafkaService:
    def __init__(self):
        self.config = {
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVER,
            "security.protocol": settings.KAFKA_SECURITY_PROTOCOL,
            "sasl.username": settings.KAFKA_SASL_USERNAME,
            "sasl.mechanisms": settings.KAFKA_SASL_MECHANISM,
            "session.timeout.ms": settings.KAFKA_SESSION_TIMEOUT_MS,
            "sasl.password": settings.KAFKA_SASL_PASSWORD,
        }

        topic = getattr(settings, "PASSPORT_KAFKA_TOPICS", "internalServerTopic")
        self.topic: list = self._build_topic_list(topic)

        extra_func_path = getattr(settings, "KAFKA_EXTRA_CONSUMING_FUNCTION", None)
        self.extra_func = import_string(extra_func_path) if extra_func_path else None


    @staticmethod
    def _build_topic_list(raw) -> List[str]:
        return [raw] if isinstance(raw, str) else raw

    def _decode_message(self, msg):
        return msg.value().decode("utf-8")

    def _extra_process(self, data):
        """
        overwrite it if there is need in extra consuming
        """
        if self.extra_func:
            self.extra_func(data)

    def process_message(self, msg):
        """
        Business logic for consuming messages
        """
        try:
            data = self._decode_message(msg)
        except UnicodeDecodeError as e:
            logger.error(e)
            return

        logger.info(f"Received message: {data}")
        try:
            data = json.loads(data)
        except ValueError as e:
            logger.error(e)
            return

        if msg.topic() == settings.PASSPORT_KAFKA_INTERNAL_SERVER_TOPIC:
            PassportKafkaService.process_message(data)
        else:
            self._extra_process(data)



    def consume_messages(self):
        """
        Default part of flow for python consumer
        """
        config = self.config

        config["group.id"] = settings.KAFKA_GROUP_ID
        config["auto.offset.reset"] = "earliest"

        # creates a new consumer and subscribes to your topic
        consumer = Consumer(config)
        consumer.subscribe(self.topic)
        try:
            while True:
                # consumer polls the topic and prints any incoming messages
                msg = consumer.poll(1.0)

                if msg is not None and msg.error() is None:
                    self.process_message(msg)
        except KeyboardInterrupt as e:
            logger.error(e)
            raise e
        finally:
            consumer.close()

    def produce_message(self, kafka_message):
        """
        Produce message to message queue. Need to implement it on a client side
        """
        producer = Producer(self.config)
        self.topic: list = self._build_topic_list(self.topic)

        producer.produce(self.topic[0], value=kafka_message)
        logger.info(f"Produced message to topic {self.topic[0]}: value = {kafka_message}")

        # send any outstanding or buffered messages to the Kafka broker
        producer.flush()


class MessageActionService:
    class Action(Enum):
        LOGOUT = "logout"
        UPDATE_USER_INFO = "update_user_info"
        BLACK_LIST_TOKEN = "black_list_token"
        START_CLEAN_UP_USER = "start_clean_up_user"
        CANCEL_CLEAN_UP_USER = "cancel_clean_up_user"
        CLEAN_UP_USER = "clean_up_user"

    def __init__(
        self,
        action: Action,
        uuid: str,
        description: str = "",
        extra=None,
        user_auth_code=None,
        service_key=None,
    ):
        if extra is None:
            extra = {}
        self.action = action
        self.uuid = str(uuid)
        self.description = description
        self.extra = extra
        self.passport = PassportUser.objects.filter(passport_uuid=uuid).first()

    def logout(self):
        """
        Action need to process after getting request for logout from a client side
        """
        if self.passport:
            logger.info(f"Consumer's message to logout: uuid - {self.uuid}")
            passport_service = PassportService(self.passport)
            passport_service.invalidate_access_tokens()
            logger.info(f"Tokens was invalidated: uuid - {self.uuid}")

    def update_user(self):
        if self.passport:
            if not self.passport.argo_user:
                logger.warning(
                    f"Argo user doesn't exist for passport - {self.passport}"
                )
                return None

            logger.info(f"Consumer's message to update_user: " f"uuid - {self.uuid}")

            # for roku users
            # if passport.argo_user is random user we need before serialize change argo_user
            # after need delete random user
            username = self.extra.get("username", "")
            email = self.extra.get("email", "")

            # match and change passport for roku users
            if username and "rokuuser_" in username.lower():
                old_passport_user = self.passport.argo_user
                # check if passport argo_user is random user
                if "@random.ra" in old_passport_user.email:
                    user = User.objects.filter(username__iexact=username).first()
                    # if we find roku user with that username we change passport argo_user
                    if user:
                        self.passport.argo_user = user
                        self.passport.save()
                        logger.info(f"Change passport {self.passport.passport_uuid} from: {old_passport_user} to {user}")
            # match and change passport from 'random' user to real
            elif email and username:
                old_passport_user = self.passport.argo_user
                if "@random.ra" in old_passport_user.email:
                    user = User.objects.filter(email__iexact=email).first()
                    if user:
                        self.passport.argo_user = user
                        self.passport.save()
                        logger.info(
                            f"Change passport {self.passport.passport_uuid} from: {old_passport_user} to {user}"
                        )

            serializer = KafkaUpdateUserSerializer(
                self.passport.argo_user, data=self.extra, partial=True, context={"uuid": self.uuid}
            )
            if serializer.is_valid():
                logger.info(f"Model user: {self.passport.argo_user}")
                try:
                    user = serializer.update(self.passport.argo_user, self.extra)
                    cache_key = format_cache_prefix(
                        settings.AUTH_USER_API_CACHE, user.id
                    )
                    invalidate_cache(cache_key)

                except BaseException as e:
                    raise e

                # Call update user hook
                on_update_user(user.id)

                logger.info(
                    f"Model user was updated: {user}, "
                    f"user was updated: uuid - {self.uuid}"
                )
            else:
                logger.error(
                    f"Passport validation error: {serializer.errors} - {self.uuid}, data={self.extra}"
                )
        else:
            logger.warning(f"Passport doesn't exist - {self.uuid}")

    def add_to_black_list(self):
        token = self.extra.get("token")
        if token:
            BlackListToken.objects.create(
                token=token,
                token_expiration=datetime.datetime.utcfromtimestamp(
                    self.extra["token_expiration"]
                ),
            )
            AccessToken.objects.filter(token=token).delete()
            logger.warning(f"Token {token} added to blacklist.")
        else:
            logger.warning(f"incorrect token - {self.extra}")

    def start_clean_up_user(self):
        """
        Start clean up user process
        """
        user = self.passport.argo_user
        user.start_delete_process()

    def cancel_clean_up_user(self):
        """
        Cancel clean up user process
        """
        user = self.passport.argo_user
        user.stop_delete_process()

    def clean_up_user(self):
        """
        Clean up user instantly
        """
        if not self.passport:
            logger.error(f"There is no passport for uuid {self.uuid }")
            return
        if not self.passport.argo_user:
            logger.error(f"There is no user for passport {self.passport.passport_uuid} ")
            self.passport.delete()
            return
        user = self.passport.argo_user
        user.clear_user_data()