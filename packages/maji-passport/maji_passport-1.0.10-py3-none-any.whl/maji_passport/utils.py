import importlib

from constance import config
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth import get_user_model
from loguru import logger


def clear_phone_number(phone):
    if phone:
        phone = str(phone).strip().replace("-", "").replace("(", "").replace(")", "")
        phone = "+" + phone if phone[0] != "+" else phone

    return phone


def get_passport_user_serializer():
    """
    Return the User model that is active in this project.
    """
    try:
        return getattr(
            importlib.import_module(settings.PASSPORT_USER_DETAILS_SERIALIZER_PATH),
            settings.PASSPORT_USER_DETAILS_SERIALIZER_CLASS,
        )
    except ValueError:
        raise ImproperlyConfigured(
            "PASSPORT_USER_DETAILS_SERIALIZER_CLASS must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "PASSPORT_USER_DETAILS_SERIALIZER_CLASS refers to model '%s' that has not been installed"
            % settings.PASSPORT_USER_DETAILS_SERIALIZER_CLASS
        )


def format_cache_prefix(prefix: str, id_: int) -> str:
    return f"{prefix}_{id_:010d}"


def invalidate_auth_cache(user):
    User_model = get_user_model()
    if user and isinstance(user, User_model) and not isinstance(user, AnonymousUser):
        user.invalidate_auth_cache()


def invalidate_cache(prefix):
    keys = cache.keys(f"*{prefix}*")
    if keys:
        for key in keys:
            cache.delete(key)
