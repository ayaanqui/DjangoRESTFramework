from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_jwt.settings import api_settings

from accounts.api.serializers import UserRegisterSerializer, UserAuthSerializer
from accounts.api.permissions import AnonymousPermissionOnly

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class AuthAPIView(APIView):
    permission_classes = [AnonymousPermissionOnly]
    serializer_class = UserAuthSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if username == "" or password == "":
            return Response({'detail': 'Make sure all fields are completed'}, status=400)

        qs = User.objects.filter(
            Q(username__iexact=username)|
            Q(email__iexact=username)
        )

        if qs.count() == 1:
            qs = qs.first()
            if qs.check_password(password):
                user = authenticate(username=qs.username, password=password)
                # login(request, user)

                # JWT token generation
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                response = jwt_response_payload_handler(token, user, request=request)
                return Response(response, status=200)
        
        return Response({"detail": "Incorret username/email or password"}, status=401)


""" class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer """


class RegisterAPIView(APIView):
    permission_classes = [AnonymousPermissionOnly]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if username == "" or email == "" or password == "":
            return Response({'detail': 'Make sure all fields are completed'}, status=400)

        # Check if username and email already exist
        username_obj = User.objects.filter(username=username)
        email_obj = User.objects.filter(email=email)

        # Form validation
        if username_obj.exists() and email_obj.exists():
            return Response([
                {
                    "username": "A user with that username already exists."
                },
                {
                    "email": "A user with that email already exists."
                }
            ], status=400)
        elif username_obj.exists():
            return Response({"username": "A user with that username already exists."}, status=400)
        elif email_obj.exists():
            return Response({"email": "A user with that email already exists."}, status=400)
        
        # Create user account
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        return Response({
            "detail": "Account created. You can now login"
        }, status=201)