"""User serializers"""

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from api.utils.fields import Base64ImageField
from users.models import Subscription


User = get_user_model()


class SignUpSerializer(UserCreateSerializer):
    """Сериализатор регистрации пользователей."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя.'
            )
        return value

    def validate(self, data):

        username = data['username']
        email = data['email']

        user = User.objects.filter(
            Q(username=username) | Q(email=email)).first()

        if user and user.email != email:
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует.'
            )
        if user and user.username != username:
            raise serializers.ValidationError(
                'Пользователь с такой почтой уже существует.'
            )
        return data


class GetUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed',
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        )
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, object):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                subscriber=request.user, author=object
            ).exists()
        return False


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для аватара"""

    avatar = Base64ImageField(allow_null=True)

    class Meta:
        model = User
        fields = ('avatar',)
