from django.contrib import admin
from django.urls import path, include
from updates import views as updatesViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('json/1/', updatesViews.MyView.as_view()),
    path('json/2/', updatesViews.MyViewMix.as_view()),
    path('json/detail/', updatesViews.SerializedDetailView.as_view()),
    path('json/list/', updatesViews.SerializedListView.as_view()),
    path('api/', include('updates.api.urls')),
    path('api/status/', include('status.api.urls')),
    path('api/auth/', include('accounts.api.urls')),
    path('api/users/', include('accounts.api.user.urls', namespace='api-user')),
]
