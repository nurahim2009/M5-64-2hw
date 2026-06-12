import random
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import UserConfirm
from .serializers import UserRegisterSerializer, UserConfirmSerializer, UserLoginSerializer

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Создаем пользователя, но делаем его НЕАКТИВНЫМ
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            is_active=False  # Комментарий из ТЗ выполнен
        )
        
        # Генерируем 6-значный рандомный код
        code = str(random.randint(100000, 999999))
        UserConfirm.objects.create(user=user, code=code)
        
        # В реальном проекте тут была бы отправка на Email, но для ДЗ выведем код в ответе
        return Response(
            {"message": "Пользователь успешно зарегистрирован! Подтвердите аккаунт.", "code": code},
            status=status.HTTP_21__CREATED if hasattr(status, 'HTTP_21__CREATED') else status.HTTP_201_CREATED
        )

class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = UserConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        code = serializer.validated_data['code']
        
        try:
            user = User.objects.get(username=username)
            if user.confirm_code.code == code:
                user.is_active = True  # Активируем клиента
                user.save()
                user.confirm_code.delete()  # Удаляем код после успешного подтверждения
                return Response({"message": "Аккаунт успешно подтвержден!"}, status=status.HTTP_200_OK)
            return Response({"error": "Неверный код подтверждения!"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден!"}, status=status.HTTP_404_NOT_FOUND)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user is not None:
            if not user.is_active:
                return Response({"error": "Ваш аккаунт не активирован! Подтвердите его кодом."}, status=status.HTTP_403_FORBIDDEN)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Неверные учетные данные!"}, status=status.HTTP_400_BAD_REQUEST)