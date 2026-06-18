from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    # Валидация для создания/изменения категории (/api/v1/categories/)
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Название категории должно содержать минимум 2 символа.")
        if len(value) > 100:
            raise serializers.ValidationError("Название категории слишком длинное (макс. 100 символов).")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']

    # Валидация заголовка товара (/api/v1/products/)
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Заголовок товара не может состоять из одних пробелов.")
        return value

    # Валидация цены товара
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена товара должна быть строго больше нуля.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']

    # Валидация текста отзыва (/api/v1/reviews/)
    def validate_text(self, value):
        if len(value).strip() < 5:
            raise serializers.ValidationError("Отзыв слишком короткий. Напишите хотя бы 5 символов.")
        return value

    # Валидация оценки
    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оценка должна быть целым числом в диапазоне от 1 до 5.")
        return value


# Дополнительный сериализатор для вывода продуктов с их отзывами
class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0.0
        return round(sum([r.stars for r in reviews]) / len(reviews), 2)