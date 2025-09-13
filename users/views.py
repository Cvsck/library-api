from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import LoginSerializer, ProfileSerializer

User = get_user_model()


@extend_schema(
    summary="Авторизация по email и паролю",
    request=LoginSerializer,
    responses={200: LoginSerializer},
    tags=["Пользователь"],
)
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)
        return Response(serializer.errors, status=400)


@extend_schema(
    summary="Профиль текущего пользователя",
    description="Возвращает email, статус и права текущего пользователя. Требуется авторизация.",
    responses={200: ProfileSerializer},
    tags=["Пользователь"],
)
class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
