from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from core.models import Recipe, ShoppingCart, Favorite
from api.serializers.shopping_cart import ShoppingCartSerializer
from api.serializers.favorite import FavoriteSerializer
from api.serializers.recipes import (
    RecipeSerializer,
    RecipeSafeSerializer,
    RecipeShortSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeSafeSerializer
        if self.action == 'shopping_cart':
            return ShoppingCartSerializer
        if self.action == 'favorite':
            return FavoriteSerializer
        return RecipeSerializer

    def add_recipe_in(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = self.get_serializer(
            data={
                'user': request.user.id,
                'recipe': recipe.id
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            RecipeShortSerializer(recipe).data,
            status=status.HTTP_201_CREATED
        )

    def remove_recipe_in(self, request, pk, model):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_in_cart = get_object_or_404(
            model, user=request.user, recipe=recipe
        )
        recipe_in_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post'],
        detail=True,
        url_path='shopping_cart',
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        return self.add_recipe_in(request, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.remove_recipe_in(request, pk, ShoppingCart)

    @action(
        methods=['post'],
        detail=True,
        url_path='favorite',
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        return self.add_recipe_in(request, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return self.remove_recipe_in(request, pk, Favorite)

    # def download_shopping_cart():
    #     pass
