from rest_framework import serializers
from .models import Recipe, RecipeCategory, Review


class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review  
        fields = ['id', 'user', 'recipe', 'rating', 'comment']
        read_only_fields = ['user', 'recipe']

class RecipeSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=RecipeCategory.objects.all())

    average_rating = serializers.FloatField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'ingredients', 'preparation_steps', 'cooking_time', 'serving_size', 'owner', 'categories','average_rating', 'reviews']
        read_only_fields = ['owner', 'average_rating', 'reviews']