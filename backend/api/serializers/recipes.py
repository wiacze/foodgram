from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from core.models import Recipe, IngredientAmount, Tag
from api.utils.fields import Base64ImageField
from api.utils.generators import generate_hash
from .tags import TagSerializer
from .users import GetUserSerializer
from .ingredients import (
    IngredientAmountSerializer,
    IngredientInRecipeSerializer,
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


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientInRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField(use_url=True, max_length=None, required=True)
    author = GetUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = RecipeShortSerializer.Meta.fields + (
            'ingredients',
            'tags',
            'text',
            'author'
        )

    @staticmethod
    def validate_items(data, message):
        if len(data) == 0:
            raise serializers.ValidationError(
                f'Количество {message[0]} должно быть больше нуля.'
            )
        items = []
        for item in data:
            if item in items:
                raise serializers.ValidationError(
                    f'{message[1]} не должны повторяться.'
                )
            items.append(item)
        return data

    def validate_tags(self, data):
        message = ('тегов', 'теги')
        return self.validate_items(data, message)

    def validate_ingredients(self, data):
        message = ('ингредиентов', 'ингредиенты')
        return self.validate_items(data, message)

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
        recipe = Recipe.objects.create(
            author=author, hash_url=generate_hash(), **validated_data
        )
        recipe.tags.set(tags)
        recipe.save()
        self.add_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        if (
            not validated_data.get('tags')
            or not validated_data.get('ingredients')
        ):
            raise serializers.ValidationError('')
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


class RecipeSafeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    author = GetUserSerializer()
    ingredients = IngredientAmountSerializer(
        source='amount_ingredients', many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = RecipeSerializer.Meta.fields + (
            'is_favorited',
            'is_in_shopping_cart',
        )

        read_only_fields = (
            'author',
            'ingredients',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, object):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.favorited.filter(recipe=object).exists()
        )

    def get_is_in_shopping_cart(self, object):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.shopping_cart.filter(recipe=object).exists()
        )


class RecipesCountSerializer(GetUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        read_only=True, source='recipes.count'
    )

    class Meta():
        model = User
        fields = GetUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, object):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        recipes = object.recipes.all()
        if recipes_limit and recipes_limit.isdigit():
            recipes = object.recipes.all()[:int(recipes_limit)]
        return RecipeShortSerializer(
            recipes, many=True, context={'request': request},
        ).data
