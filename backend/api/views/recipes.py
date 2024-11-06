from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Recipe, ShoppingCart, Favorite, IngredientAmount
from api.permissions import IsAdminIsAuthorOrReadOnly
from api.filters import RecipeFilter
from api.utils.generators import generate_shopping_list
from api.serializers.favorite_shopping_cart import (
    FavoriteSerializer,
    ShoppingCartSerializer,
)
from api.serializers.recipes import (
    RecipeSerializer,
    RecipeSafeSerializer,
    RecipeShortSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    permission_classes = (
        IsAdminIsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

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

    def remove_recipe_in(self, request, pk, model, message):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_in = model.objects.filter(user=request.user, recipe=recipe)
        if recipe_in.exists():
            recipe_in.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': f'Вы не добавляли этот рецепт в {message}.'},
            status=status.HTTP_400_BAD_REQUEST
        )

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
        return self.remove_recipe_in(
            request, pk, ShoppingCart, 'список покупок'
        )

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
        return self.remove_recipe_in(
            request, pk, Favorite, 'избранное'
        )

    @action(
        methods=['get'],
        detail=False,
        url_path='download_shopping_cart',
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientAmount.objects
            .filter(recipe__shopping_cart__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
            .order_by('ingredient__name')
        )
        return generate_shopping_list(ingredients)

    @action(
        methods=['get'],
        detail=True,
        url_path='get-link',
        url_name='get-link',
    )
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        short_link = request.build_absolute_uri(f'/s/{recipe.hash_url}/')
        return Response({'short-link': short_link}, status=status.HTTP_200_OK)
