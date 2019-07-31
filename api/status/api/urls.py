from django.urls import path

from status.api.views import (
    StatusAPIView,
    StatusDetailAPIView
)

urlpatterns = [
    path('', StatusAPIView.as_view()),
    path('<int:id>/', StatusDetailAPIView.as_view(), name='status-detail')
]