from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ReviewViewSet, RegisterAPIView, ConfirmAPIView, LoginAPIView

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')
router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    # Новые эндпоинты для ДЗ-5:
    path('users/register/', RegisterAPIView.as_view()),
    path('users/confirm/', ConfirmAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
]