from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, URLField
from rest_framework.serializers import Serializer, ModelSerializer

from maji_passport.services.passport import PassportService, has_passport

User = get_user_model()


class UserPassportSetPasswordSerializer(Serializer):
    password = CharField()

    def validate(self, attrs):
        user = self.context["request"].user
        if user.check_password(attrs["password"]) is False:
            raise ValidationError("Wrong password")
        return attrs


class GetLoginUrlOutputSerializer(Serializer):
    url = URLField()


class CommonUserPassportUpdateSerializer(ModelSerializer):
    avatar_url = CharField(required=False)
    cover_url = CharField(required=False)
    display_name = CharField(required=False)
    about = CharField(required=False)
    social_networks = CharField(required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "avatar_url",
            "cover_url",
            "email",
            "display_name",
            "about",
            "social_networks",
        )

    def to_internal_value(self, data):
        """
        Remove empty social networks keys from social_networks
        """
        result = data.copy()

        if social_networks := data.get("social_networks"):
            for key in settings.SOCIAL_PLATFORMS.keys():
                if (
                    key in social_networks.copy().keys() and
                    not social_networks.copy().get(key)
                ):
                    social_networks.pop(key, None)
            result["social_networks"] = social_networks
        return result


class UserPassportUpdateSerializer(CommonUserPassportUpdateSerializer):
    def update(self, instance, validated_data):
        passport_data = {}
        validated_data = validated_data.copy()  # we change validated data from immutable to mutable
        avatar_url = validated_data.pop("avatar_url", None)
        cover_url = validated_data.pop("cover_url", None)
        if avatar_url:
            passport_data["avatar_url"] = avatar_url.split("?")[0]  # clean image storage parameters
        if cover_url:
            passport_data["cover_url"] = cover_url.split("?")[0]  # clean image storage parameters
        if "username" in validated_data:
            passport_data["username"] = validated_data["username"]
        if "email" in validated_data:
            # pop email from validated_data bcs email change in passport
            new_email = validated_data.pop("email")
            # add to extra
            instance.extra["email_change_to"] = new_email
            # add to passport_data
            passport_data["email"] = new_email
        if "display_name" in validated_data:
            passport_data["display_name"] = validated_data["display_name"]
        if "social_networks" in validated_data:
            passport_data["social_networks"] = validated_data["social_networks"]
        if has_passport(instance):
            PassportService.send_data_to_passport(instance.passport_user, passport_data)

        instance = super().update(instance, validated_data)
        return instance