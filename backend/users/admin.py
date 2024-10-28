"""Admin zone of subscriptions and users"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.admin import TokenProxy

from .models import Subscription


User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
    )
    list_filter = (
        'username',
        'email',
    )
    # list_editable = ()
    list_display_links = (
        'id',
        'username',
    )
    list_per_page = 10


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'subscriber',
    )
    search_fields = (
        'author',
    )
    list_filter = (
        'author',
    )
    list_per_page = 10


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
