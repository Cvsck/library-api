from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# -------------------------------
# CustomTokenObtainPairSerializer — вход по email и паролю
# -------------------------------
class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Неверный email или пароль.")

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


# -------------------------------
# CustomTokenObtainPairView — аннотированный эндпоинт /api/catalog/token/
# -------------------------------
@extend_schema(
    summary="Получение JWT токена",
    description="Возвращает access и refresh токены по email и паролю.",
    request=CustomTokenObtainPairSerializer,
    responses={200: CustomTokenObtainPairSerializer},
    tags=["Аутентификация"],
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# -------------------------------
# CustomTokenRefreshView — аннотированный эндпоинт /api/catalog/token/refresh/
# -------------------------------
@extend_schema(
    summary="Обновление access токена",
    description="Принимает refresh токен и возвращает новый access токен.",
    tags=["Аутентификация"],
)
class CustomTokenRefreshView(TokenRefreshView):
    pass
