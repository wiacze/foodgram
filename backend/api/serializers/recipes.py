from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from api.utils.fields import Base64ImageField
from core.models import Recipe, IngredientAmount, Tag
from .tags import TagSerializer
from .users import GetUserSerializer
from .ingredients import (
    IngredientAmountSerializer,
    IngredientAmountShortSerializer,
)


User = get_user_model()


class RecipeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class RecipeSafeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    author = GetUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True,
        default=False
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    @staticmethod
    def get_ingredients(object):
        ingredients = IngredientAmount.objects.filter(recipe=object)
        return IngredientAmountSerializer(ingredients, many=True).data

    def get_is_favorited(self, object):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return request.user.favorited.filter(recipe=object).exists()

    def get_is_in_shopping_cart(self, object):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return request.user.shopping_cart.filter(recipe=object).exists()


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountShortSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField(use_url=True, max_length=None)
    author = GetUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author'
        )

    # def validate_image(self, value):
    #     pass

    # def validate_tags(self, value):
    #     pass

    # def validate_ingredients(self, value):
    #     pass

    # def validate_cooking_time(self, value):
    #     pass

    @staticmethod
    def add_ingredients(recipe, ingredients):
        IngredientAmount.objects.bulk_create([
            IngredientAmount(
                ingredient=ingredient.get('ingredient'),
                recipe=recipe,
                amount=ingredient.get('amount')
            )
            for ingredient in ingredients
        ])

    @transaction.atomic
    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        recipe.save()
        self.add_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.ingredients.clear()
        instance.tags.set(tags)
        self.add_ingredients(instance, ingredients)
        super().update(instance, validated_data)
        return instance

    def to_representation(self, value):
        serializer = RecipeSafeSerializer(value, context=self.context)
        return serializer.data


class RecipesCountSerializer(GetUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        read_only=True, source='recipes.count'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar',
        )

    def get_recipes(self, object):
        recipes = object.recipes.all()
        return RecipeShortSerializer(recipes, many=True).data
