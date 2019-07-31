from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from status.models import Status
from status.api.serializers import StatusSerializer
from accounts.api.permissions import IsOwnerOrReadOnly


""" class StatusListSearchAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        qs = Status.objects.all()
        serializedData = StatusSerializer(qs, many=True)
        return Response(serializedData.data) """


class StatusAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = StatusSerializer

    def get_queryset(self):
        qs = Status.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StatusDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    lookup_field = 'id'

    # Use get_object method or lookup_field
    """ def get_object(self, *args, **kwargs):
        id = self.kwargs.get('id')
        return Status.objects.get(id=id) """
    
    def put(self, request,  *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    """ def patch(self, request,  *args, **kwargs):
        return self.update(request, *args, **kwargs) """
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)