from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import LoginSerializer


@extend_schema(
    summary="Авторизация по email и паролю",
    request=LoginSerializer,
    responses={200: LoginSerializer},
)
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)
        return Response(serializer.errors, status=400)


User = get_user_model()


@extend_schema(
    summary="Профиль текущего пользователя",
    description="Возвращает email, статус и права текущего пользователя. Требуется авторизация.",
    responses={200: dict},
)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "email": user.email,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "is_active": user.is_active,
            }
        )
