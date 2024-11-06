from rest_framework import serializers

from foodgram_backend import constants
from core.models import Ingredient, IngredientAmount


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')

    def validate_amount(self, value):
        if value < constants.MIN_VALUE:
            raise serializers.ValidationError(
                constants.INVALID_MIN_MESSAGE
            )
        if value > constants.MAX_VALUE:
            raise serializers.ValidationError(
                constants.INVALID_MAX_MESSAGE
            )
        return value


class IngredientAmountSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')
