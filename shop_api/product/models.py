from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# 1. Категории
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 2. Товары
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title

# 3. Отзывы
class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"Отзыв ({self.stars}⭐) для {self.product.title}"

# 4. Подтверждение пользователей (Новое для ДЗ-5)
class UserConfirm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirm_code')
    code = models.CharField(max_length=6)

    def __str__(self):
        return f"Код {self.code} для {self.user.username}"