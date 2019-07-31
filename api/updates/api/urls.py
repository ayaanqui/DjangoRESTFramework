from django.urls import path
from updates.api.views import (
                UpdatesModelDetailAPIView,
                UpdatesModelListAPIView    
)

urlpatterns = [
    path('updates/<int:id>/', UpdatesModelDetailAPIView.as_view()),
    path('updates/', UpdatesModelListAPIView.as_view(), name='updates-list-view')
]