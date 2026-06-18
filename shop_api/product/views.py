import random
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from .models import Category, Product, Review, UserConfirm
from .serializers import (
    CategorySerializer, ProductSerializer, ReviewSerializer, 
    ProductReviewsSerializer, UserRegisterSerializer, 
    UserConfirmSerializer, UserLoginSerializer
)

# ==================== СУЩЕСТВУЮЩИЕ VIEWSETS (УЖЕ CBV) ====================

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'], url_path='reviews')
    def products_with_reviews(self, request):
        products = self.get_queryset()
        serializer = ProductReviewsSerializer(products, many=True)
        return Response(serializer.data)

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# ==================== НОВЫЕ ВЬЮШКИ ПОЛЬЗОВАТЕЛЕЙ НА CBV ====================

class RegisterGenericAPIView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            is_active=False  # Пользователь изначально неактивен
        )
        
        # Генерация 6-значного кода
        code = str(random.randint(100000, 999999))
        UserConfirm.objects.create(user=user, code=code)
        
        return Response(
            {"message": "Пользователь зарегистрирован! Подтвердите аккаунт.", "code": code},
            status=status.HTTP_201_CREATED
        )


class ConfirmGenericAPIView(generics.GenericAPIView):
    serializer_class = UserConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        code = serializer.validated_data['code']
        
        try:
            user = User.objects.get(username=username)
            if user.confirm_code.code == code:
                user.is_active = True
                user.save()
                user.confirm_code.delete()  # Удаляем код после успешной активации
                return Response({"message": "Аккаунт успешно подтвержден!"}, status=status.HTTP_200_OK)
            return Response({"error": "Неверный код подтверждения!"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден!"}, status=status.HTTP_404_NOT_FOUND)


class LoginGenericAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user is not None:
            if not user.is_active:
                return Response({"error": "Ваш аккаунт не активирован! Введите код подтверждения."}, status=status.HTTP_403_FORBIDDEN)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Неверные учетные данные!"}, status=status.HTTP_400_BAD_REQUEST)