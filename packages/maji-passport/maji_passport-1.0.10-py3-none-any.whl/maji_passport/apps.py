from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PassportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maji_passport"
    verbose_name = _("Maji Passport")
