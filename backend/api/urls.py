from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.users import CustomUserViewSet
from api.views.tags import TagViewSet
from api.views.ingredients import IngredientViewSet
from api.views.recipes import RecipeViewSet


router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
