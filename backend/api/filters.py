from django.contrib.auth import get_user_model
from django_filters.rest_framework import (
    BooleanFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
)
from rest_framework.filters import SearchFilter

from core.models import Recipe, Tag


User = get_user_model()


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):

    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = BooleanFilter(
        method='is_favorite_filter',
    )
    is_in_shopping_cart = BooleanFilter(
        method='is_in_shopping_cart_filter'
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def is_favorite_filter(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(favorited__user=user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return queryset
