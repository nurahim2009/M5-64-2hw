from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, ReviewViewSet, 
    RegisterGenericAPIView, ConfirmGenericAPIView, LoginGenericAPIView
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')
router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    # Маршруты на обновленных классах CBV:
    path('users/register/', RegisterGenericAPIView.as_view(), name='user-register'),
    path('users/confirm/', ConfirmGenericAPIView.as_view(), name='user-confirm'),
    path('users/login/', LoginGenericAPIView.as_view(), name='user-login'),
]
