from django.contrib.auth.models import User

from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]
        extra_kwargs = {
            'password': {
                'style': {
                    'input_type': 'password'
                },
                'write_only': True
            }
        }


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {
                'style': {
                    'input_type': 'password'
                },
                'write_only': True
            }
        }