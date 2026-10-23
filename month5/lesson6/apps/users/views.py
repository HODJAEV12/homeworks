from django.contrib.auth import login, logout
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .tokens import jwt_payload, token_payload, user_payload

# ---------------- REGISTER ------------------------

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'message': 'Пользователь успешно зарегистрирован',
                'user': UserSerializer(user).data,
                'tokens': {
                    'jwt': jwt_payload(user),
                    'token': token_payload(user('token')),
                }
            },
            status=status.HTTP_201_CREATED
        )

# ---------------- TOKEN ------------------------

class TokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        return Response(token_payload(user), status=status.HTTP_201_CREATED)

class TokenLogOutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()

        return Response({
            'message': 'Токен успешно удалён'
        }, status=status.HTTP_200_OK)

# ---------------- JWT ------------------------

class JWTView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        return Response(jwt_payload(user), status=status.HTTP_200_OK)

class JWTLogOutView(TokenRefreshView):
    permission_classes = [permissions.IsAuthenticated]

# ---------------- Login/Logout ------------------------

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        return Response(
            {
                "message": f"Вы успешно вошли в систему, {user.username}",
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )

class LogOutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {
                "message": "Вы успешно вышли из аккаунта",
            },
            status=status.HTTP_200_OK
        )

# ---------------- Profile ------------------------

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
