import secrets
import uuid
from datetime import timedelta, datetime

import pytest
from django.utils import timezone
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient

from maji_passport.models import PassportUser, AccessToken


@pytest.mark.django_db
@pytest.mark.passport
@override_settings(
    PASSPORT_SERVICE_KEY="test_key",
    PASSPORT_EXCHANGE_URL="http://test.com/exchange/",
    PASSPORT_EXTRA_TOKEN_URL="http://test.com/extra_token/",
    PASSPORT_START_MIGRATE="http://test.com/start",
    PASSPORT_UPDATE_TOKEN_URL="http://test.com/api/v1/internal_auth/auth/update_token/",
    PASSPORT_SET_PASSWORD="http://test.com/set_pass",
)
def test_exchange(create_user, auth_fabric, faker, mocker):
    passport_user_uuid = uuid.uuid4()
    user_auth_code = secrets.token_hex(16)
    access_token = secrets.token_hex(32)
    access_token_expiration = datetime.now() + timedelta(hours=20)
    refresh_token = secrets.token_hex(32)
    mocker.patch(
        "passport.services.exchange.ExchangeTokenService.send_post_request",
        return_value={
            "user_uuid": passport_user_uuid,
            "user_auth_code": user_auth_code,
            "access_token": access_token,
            "access_token_expiration": str(access_token_expiration),
            "refresh_token": refresh_token,
        },
    )
    mocker.patch(
        "passport.services.exchange.ExchangeTokenService.save_tokens",
        return_value=True,
    )

    u_requester = create_user(
        email=faker.email(),
        registered_at=timezone.now(),
        is_registered=True,
        username="test_username",
    )

    api_client_unregistered = APIClient()
    data = {
        "email": u_requester.email,
        "user_auth_code": user_auth_code,
        "user_uuid": passport_user_uuid,
        "username": u_requester.username,
    }
    response = api_client_unregistered.post(f"/api/auth/external/exchange/", data=data)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_working_with_passport_token(create_user, auth_fabric, faker, mocker):
    passport_user_uuid = uuid.uuid4()
    user_auth_code = secrets.token_hex(16)
    access_token = secrets.token_hex(32)
    refresh_token = secrets.token_hex(32)
    new_access_token = secrets.token_hex(32)

    mocker.patch(
        "passport.services.exchange.ExchangeTokenService.update_token_by_refresh",
        return_value=new_access_token,
    )

    u_requester = create_user(
        email=faker.email(),
        registered_at=timezone.now(),
        is_registered=True,
        username="test_username",
    )

    passport = PassportUser.objects.create(
        user_auth_code=user_auth_code,
        refresh_token=refresh_token,
        argo_user=u_requester,
        passport_uuid=passport_user_uuid,
    )

    access_token_obj = AccessToken.objects.create(
        passport_user=passport,
        token=access_token,
        target="main",
    )

    api_client_unregistered = APIClient()

    response = api_client_unregistered.get(
        f"/api/auth/user/",
        HTTP_AUTHORIZATION=f"Bearer {access_token}",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = api_client_unregistered.post(
        f"/api/auth/passport/update_token/",
        HTTP_AUTHORIZATION=f"Bearer {access_token}",
    )

    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]

    # part of the mock. We can update expiration only by passport
    access_token_obj.token = token
    access_token_obj.token_expiration = datetime.now() + timedelta(days=2)
    access_token_obj.save()

    response = api_client_unregistered.get(
        f"/api/auth/user/",
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    assert response.status_code == status.HTTP_200_OK

    response = api_client_unregistered.post(
        f"/api/auth/passport/update_token/",
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
