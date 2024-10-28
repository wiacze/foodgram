from rest_framework import serializers, validators

from users.models import Subscription
from .recipes import RecipesCountSerializer


class SubscribtionSerializer(serializers.ModelSerializer):

    # subscriber = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='email',
    #     default=serializers.CurrentUserDefault(),
    # )
    # author = serializers.SlugRelatedField(
    #     slug_field='email',
    #     queryset=User.objects.all(),
    # )

    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('subscriber', 'author'),
                message='Вы уже подписались на этого автора.'
            )
        ]

    def validate(self, data):
        if data['subscriber'] == data['author']:
            raise serializers.ValidationError(
                'Невозможно подписаться на самого себя.'
            )
        return data

    def to_representation(self, instance):
        return RecipesCountSerializer(
            instance.author, context=self.context
        ).data
