import json
import secrets
import uuid

import pytest
from django.utils import timezone
from django.test import override_settings

from maji_passport.models import PassportUser
from maji_passport.services.kafka import KafkaService


@pytest.mark.django_db
@pytest.mark.passport
@override_settings(
    PASSPORT_SERVICE_KEY="test_key",
)
def test_kafka(create_user, auth_fabric, faker, mocker):
    user_auth_code = secrets.token_hex(16)
    return_value = {
        "action": "logout",
        "user_auth_code": user_auth_code,
        "description": "test_description",
        "service_key": "test_key",
    }
    return_value = json.dumps(return_value)
    mocker.patch(
        "passport.services.kafka.KafkaService._decode_message",
        return_value=return_value,
    )

    passport_user_uuid = uuid.uuid4()

    u_requester = create_user(
        email=faker.email(),
        username=faker.name(),
        registered_at=timezone.now(),
        is_registered=True,
    )
    PassportUser.objects.create(
        argo_user=u_requester,
        user_auth_code=user_auth_code,
        passport_uuid=passport_user_uuid,
    )

    service = KafkaService()
    service.process_message("")

    new_username = "test_change"
    return_value = {
        "action": "update_user_info",
        "user_auth_code": user_auth_code,
        "description": "test_description",
        "service_key": "test_key",
        "extra": {"username": new_username},
    }
    return_value = json.dumps(return_value)

    mocker.patch(
        "passport.services.kafka.KafkaService._decode_message",
        return_value=return_value,
    )
    service.process_message("")
    new_passport = PassportUser.objects.get(user_auth_code=user_auth_code)
    assert new_passport.argo_user.username == new_username
    assert new_passport.argo_user.display_name == new_username

    new_phone = "+66949739301"
    same_user_with_that_phone = create_user(
        email=faker.email(),
        username=faker.name(),
        registered_at=timezone.now(),
        is_registered=True,
        phone=new_phone,
        is_phone_verified=True,
    )

    return_value = {
        "action": "update_user_info",
        "user_auth_code": user_auth_code,
        "description": "test_description",
        "service_key": "test_key",
        "extra": {
            "mobile": new_phone,
            "token": "1234",
            "phone": new_phone,
            "is_phone_verified": True,
        },
    }
    return_value = json.dumps(return_value)

    mocker.patch(
        "passport.services.kafka.KafkaService._decode_message",
        return_value=return_value,
    )
    service.process_message("")
    new_passport = PassportUser.objects.get(user_auth_code=user_auth_code)
    assert new_passport.argo_user.phone == new_phone
    assert new_passport.argo_user.is_phone_verified is True

    same_user_with_that_phone.refresh_from_db()
    assert str(same_user_with_that_phone.phone) == ""
    assert same_user_with_that_phone.is_phone_verified is False
