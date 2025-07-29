from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import HashIndex
from django.db.models import (
    SET_NULL,
    CharField,
    DateTimeField,
    ForeignKey,
    TextChoices,
    OneToOneField,
    CASCADE, Model,
)
from django.db.models.fields import UUIDField, TextField
from django.utils import timezone

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField
User = get_user_model()


class BaseModel(Model):
    class Meta:
        abstract = True

    created_at = DateTimeField(auto_now_add=True, db_index=True)
    updated_at = DateTimeField(auto_now=True, db_index=True)
    extra = JSONField(default=dict, blank=True, null=True)


class PassportUser(BaseModel):
    argo_user = OneToOneField(User, null=True, on_delete=SET_NULL, related_name="passport_user")
    passport_uuid = UUIDField(null=False, unique=True)
    user_auth_code = CharField(max_length=255, null=False)
    refresh_token = TextField()
    avatar_url = CharField(max_length=255, blank=True, null=True)
    cover_url = CharField(max_length=255, blank=True, null=True)
    display_name = CharField(max_length=255, blank=True, null=True)
    social_networks = JSONField(blank=True, null=True)

    def __str__(self):
        if self.argo_user:
            return (
                f"argo email - {self.argo_user.email}, passport uuid - {self.passport_uuid}"
            )
        return f"passport uuid - {self.passport_uuid}"


class TargetAccess(TextChoices):
    MAIN = "main", "Main"
    Android = "android", "Android"
    ROKU = "roku", "Roku"
    EXTRA = "extra", "Extra"


class AccessToken(BaseModel):
    class Meta:
        indexes = (HashIndex(fields=("token",)),)

    passport_user = ForeignKey(PassportUser, null=True, on_delete=CASCADE)
    token = TextField()
    token_expiration = DateTimeField(default=timezone.now)
    target = CharField(
        max_length=30, choices=TargetAccess.choices, default=TargetAccess.MAIN
    )

    def __str__(self):
        return f"Access token for: {self.passport_user}"

    @property
    def is_token_expired(self) -> bool:
        return self.token_expiration < datetime.now(self.token_expiration.tzinfo)


class BlackListToken(BaseModel):
    class Meta:
        indexes = (HashIndex(fields=("token",)),)

    token = TextField()
    token_expiration = DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Black list token for: {self.token}"
