from django.shortcuts import reverse

from rest_framework import serializers

from status.models import Status
from accounts.api.user.serializers import UserDetailSerializer, UserListSerializer


class StatusSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Status
        fields = [
            'id',
            'user', 
            'content',
            'image',
            'timestamp',
            'url'
        ]
        read_only_fields = ['user', 'url']
    
    def get_url(self, obj):
        return reverse('status-detail', args=(obj.id,))
    
    """ def validate_content(self, value):
        if len(value) > 1000:
            raise serializers.ValidationError("The status is too long.")
        return value """
    
    def validate(self, data):
        content = data.get('content', None)
        if content == "":
            content = None
        image = data.get('image', None)

        if content is None and image is None:
            raise serializers.ValidationError("Content or Image is required.")
        return data


class StatusUserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Status
        fields = [
            'id',
            'content',
            'image',
            'url'
        ]
    
    def get_url(self, obj):
        return reverse('status-detail', args=(obj.id,))