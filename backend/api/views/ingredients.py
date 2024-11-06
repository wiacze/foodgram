from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Ingredient
from api.serializers.ingredients import IngredientSerializer
from api.filters import IngredientSearchFilter
from api.permissions import IsAdminIsAuthorOrReadOnly


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminIsAuthorOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    # Заменить на '@name' после перехода на postgresql в продакшене
    pagination_class = None
