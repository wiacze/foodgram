"""Admin zone of core models"""

from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    IngredientAmount,
    Favorite,
    Recipe,
    ShoppingCart,
)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    list_filter = ('name',)
    list_display_links = ('name',)
    list_per_page = 10


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)
    list_per_page = 10


class IngredientAmountAdmin(admin.ModelAdmin):
    pass


class FavoriteAdmin(admin.ModelAdmin):
    pass


class RecipeAdmin(admin.ModelAdmin):
    pass


class ShoppingCartAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
# admin.site.register(IngredientAmount, IngredientAmountAdmin)
# admin.site.register(Favorite, FavoriteAdmin)
# admin.site.register(Recipe, RecipeAdmin)
# admin.site.register(ShoppingCart, ShoppingCartAdmin)
