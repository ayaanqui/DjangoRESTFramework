from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from accounts.api.user.serializers import UserDetailSerializer, UserListSerializer

class UserListAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.filter(is_active=True)

    def get_queryset(self, *args, **kwargs):
        q = self.request.GET.get('q', None)
        if q is not None:
            qs = User.objects.filter(
                Q(username__icontains=q)|
                Q(email__icontains=q)
            )
            return qs
        return User.objects.all()

class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.filter(is_active=True)
    lookup_field = 'username'

    def get_serializer_context(self):
        return {'request': self.request}
    