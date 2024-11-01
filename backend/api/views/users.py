from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Subscription
from api.serializers.users import AvatarSerializer
from api.serializers.subscriptions import SubscribtionSerializer


User = get_user_model()


class CustomUserViewSet(UserViewSet):

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    def change_avatar(self, data):
        instance = self.get_instance()
        serializer = AvatarSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

    @action(
        methods=['put'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='me/avatar',
        url_name='me-avatar',
    )
    def avatar(self, request):
        serializer = self.change_avatar(request.data)
        return Response(serializer.data)

    @avatar.mapping.delete
    def delete_avatar(self, request):
        self.change_avatar({'avatar': None})
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions',
        url_name='Subscriptions',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def get_subscriptions(self, request):
        subscriptions = Subscription.objects.filter(
            subscriber=self.request.user
        )
        pages = self.paginate_queryset(subscriptions)
        serializer = SubscribtionSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post'],
        url_path='subscribe',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        serializer = SubscribtionSerializer(
            data={'subscriber': request.user.id, 'author': author.id},
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        subscription = Subscription.objects.filter(
            subscriber=request.user, author=author
        )
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
