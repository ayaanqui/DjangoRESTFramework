import datetime
from django.utils import timezone
from django.conf import settings

from rest_framework_jwt.settings import api_settings

from accounts.api.user.serializers import UserSerializer


expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user).data,
        'expires': timezone.now() + expire_delta - datetime.timedelta(seconds=200)
    }