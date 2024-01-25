# Example views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            print("user", user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        print("user", user)
        print("user.password", user.password)
        user.set_password(serializer.validated_data['password'])
        user.save()
        Token.objects.create(user=user)

# {
#     "username": "ayush",
#     "email": "ayush@gmail.com",
#     "password": "Ayush123#"
# }