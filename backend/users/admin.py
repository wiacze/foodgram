"""Admin zone of subscriptions and users."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.admin import TokenProxy

from foodgram_backend.constants import USERS_PER_PAGE, SUBS_PER_PAGE
from .models import Subscription


User = get_user_model()


class CustomUserAdmin(UserAdmin):
    """Администрирование пользователей."""

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Персональная информация'), {
            'fields': ('first_name', 'last_name', 'email', 'avatar')
        }),
        (('Права доступа'), {
            'fields': (
                'is_active', 'is_superuser', 'is_admin', 'user_permissions'
            ),
        }),
        (('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_admin',
    )
    list_display_links = ('id', 'username', 'email',)
    list_editable = ('is_admin',)
    list_filter = ('is_admin', 'is_active',)
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    ordering = ('id',)
    list_per_page = USERS_PER_PAGE


class SubscriptionAdmin(admin.ModelAdmin):
    """Администрирование подписок."""

    list_display = (
        'id',
        'author',
        'subscriber',
    )
    list_filter = ('author', 'subscriber',)
    search_fields = ('author', 'subscriber',)
    list_per_page = SUBS_PER_PAGE


admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
