from django.contrib import admin

from maji_passport.models import PassportUser, AccessToken, BlackListToken


@admin.register(PassportUser)
class PassportUserAdmin(admin.ModelAdmin):
    readonly_fields = ("argo_user",)
    search_fields = ("argo_user__email", "user_auth_code", "passport_uuid")


@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    readonly_fields = ("token", "token_expiration", "passport_user")
    search_fields = ("passport_user__argo_user__email", "passport_user__passport_uuid")


@admin.register(BlackListToken)
class BlackListTokenAdmin(admin.ModelAdmin):
    list_display = (
        "token",
        "token_expiration",
    )

