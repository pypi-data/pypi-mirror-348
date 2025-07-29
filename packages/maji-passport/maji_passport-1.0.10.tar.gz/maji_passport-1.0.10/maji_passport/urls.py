from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from maji_passport.views.exchange import (
    ExchangeTokenViewSet,
    ServiceToken,
    UpdateUserInfoViewSet,
    ServiceLoginViewSet, UpdateTokenV2,
)
from maji_passport.views.passport import (
    UserPassportViewSet,
    PassportViewSet,
    DeleteUserView,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(
    "passport", UserPassportViewSet, basename="user_merge_passport_password"
)
router.register("passport", PassportViewSet, basename="passport")

router.register("external", ExchangeTokenViewSet, basename="exchange_token")
router.register("external", ServiceToken, basename="service_token")
router.register("external", ServiceLoginViewSet, basename="external_ping_login")

router.register(
    "external/update_user", UpdateUserInfoViewSet, basename="update_user_info"
)

urlpatterns = [
    path("external/v2/update_token/", UpdateTokenV2.as_view(), name="update_token_v2"),
    path("external/delete_user/", DeleteUserView.as_view(), name="delete_user"),
]
urlpatterns += router.urls
