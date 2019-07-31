from django.urls import path, include

from accounts.api.views import AuthAPIView, RegisterAPIView

# JWT
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('', AuthAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('jwt/', obtain_jwt_token),
    path('refresh/', refresh_jwt_token),
]