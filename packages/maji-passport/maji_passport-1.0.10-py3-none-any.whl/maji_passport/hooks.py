import loguru
from django.conf import settings
from django.utils.module_loading import import_string


def on_update_user(user_id: int):
    """
    Hook on update user email
    """
    path_to_hook = getattr(settings, "PASSPORT_ON_UPDATE_USER_HOOK")
    if not path_to_hook:
        return

    try:
        on_update_user_hook = import_string(path_to_hook)
        on_update_user_hook(user_id)
    except Exception as e:
        loguru.logger.warning(f"HOOK on update user exception: {e}")


def on_register_user(user_uuid: str, email: str):
    """
    Hook on update user email
    """
    path_to_hook = getattr(settings, "PASSPORT_ON_REGISTER_USER_HOOK")
    if not path_to_hook:
        return

    try:
        on_register_user_hook = import_string(path_to_hook)
        on_register_user_hook(user_uuid, email)
    except Exception as e:
        loguru.logger.warning(f"HOOK on register user exception: {e}")