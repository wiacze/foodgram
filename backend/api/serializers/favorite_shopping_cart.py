from rest_framework import serializers

from core.models import Favorite, ShoppingCart


class UserRecipeSerializer(serializers.ModelSerializer):

    _model_name: str = None

    class Meta:
        model = None
        fields = '__all__'

    def validate(self, data):
        recipe = data['recipe']
        user = self.context['request'].user
        if self.Meta.model.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                f'Рецепт уже добавлен в {self._model_name}.'
            )
        return data


class FavoriteSerializer(UserRecipeSerializer):

    _model_name = 'избранное'

    class Meta(UserRecipeSerializer.Meta):
        model = Favorite


class ShoppingCartSerializer(UserRecipeSerializer):

    _model_name = 'список покупок'

    class Meta(UserRecipeSerializer.Meta):
        model = ShoppingCart
