from rest_framework import viewsets, permissions

from core.models import Tag
from api.serializers.tags import TagSerializer
from api.permissions import IsAdminIsAuthorOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminIsAuthorOrReadOnly,)
    pagination_class = None
