"""Admin zone of core models."""

from django.contrib import admin

from foodgram_backend.constants import (
    INGREDIENTS_PER_PAGE,
    TAGS_PER_PAGE,
    RECIPES_PER_PAGE,
)
from .models import (
    Tag,
    Ingredient,
    IngredientAmount,
    Recipe,
    Favorite,
)


class IngredientSearch(admin.ModelAdmin):
    search_fields = ('ingredient__name',)

    class Meta:
        model = IngredientAmount


class IngredientsInline(admin.TabularInline):

    model = IngredientAmount
    extra = 1
    min_num = 1
    autocomplete_fields = ('ingredient',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    list_display_links = ('name',)
    ordering = ('id', 'name', 'measurement_unit',)
    list_per_page = INGREDIENTS_PER_PAGE


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
    ordering = ('id',)
    list_per_page = TAGS_PER_PAGE


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                ('name', 'cooking_time', 'author', 'pub_date'),
                'text',
                'image',
                'tags',
                ('hash_url', 'favorite_count',),
            ),
        }),
    )
    filter_horizontal = ('tags',)
    list_filter = ('tags',)
    list_display = (
        'id', 'name', 'author', 'cooking_time', 'pub_date'
    )
    search_fields = ('id', 'name', 'author__username', 'author__email',)
    readonly_fields = ('favorite_count', 'pub_date',)
    list_display_links = ('id', 'name',)
    list_per_page = RECIPES_PER_PAGE
    ordering = ('-pub_date', 'author', 'id',)
    inlines = [IngredientsInline]

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


class IngredientAmounAdmin(admin.ModelAdmin):
    pass


class FavoriteAdmin(admin.ModelAdmin):
    pass


class ShoppingCartAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
