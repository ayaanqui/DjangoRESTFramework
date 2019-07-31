from django.urls import path

from accounts.api.user.views import UserDetailAPIView, UserListAPIView

app_name = "api-user"
urlpatterns = [
    path('', UserListAPIView.as_view(), name="list"),
    path('<str:username>/', UserDetailAPIView.as_view(), name="detail")
]