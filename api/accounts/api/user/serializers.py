from django.contrib.auth.models import User
from django.shortcuts import reverse

from rest_framework import serializers

from status.models import Status


class UserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'is_active',
            'url'
        ]
    
    def get_url(self, obj):
        return reverse('api-user:detail', args=(obj.username,))


class UserListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'url'
        ]
    
    def get_url(self, obj):
        return reverse('api-user:detail', args=(obj.username,))


class UserDetailSerializer(serializers.ModelSerializer):
    status_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'status_list'
        ]
    
    def get_status_list(self, obj):
        from status.api.serializers import StatusUserSerializer

        request = self.context.get('request')
        limit = 10
        if request:
            limit_q = request.GET.get('limit')
            try:
                limit = int(limit_q)
            except:
                pass

        qs = Status.objects.filter(user=obj.id).order_by('-timestamp')
        return StatusUserSerializer(qs[:limit], many=True).data