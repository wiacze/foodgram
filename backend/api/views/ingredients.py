from rest_framework import viewsets

from core.models import Ingredient
from api.serializers.ingredients import IngredientSerializer
from api.filters import IngredientSearchFilter
from api.permissions import IsAdminIsAuthorOrReadOnly


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminIsAuthorOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('@name',)  # '@name' для PostgeSQL, '^name' для SQLite
    pagination_class = None
