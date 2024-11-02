"""User model for FOODGRAM PROJECT."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from foodgram_backend import constants


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=constants.USERFIELDS_LENGTH,
        unique=True,
        validators=[
            RegexValidator(constants.USER_REGEX),
        ],
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=constants.EMAIL_LENGTH,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=constants.USERFIELDS_LENGTH,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=constants.USERFIELDS_LENGTH,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=constants.USERFIELDS_LENGTH,
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='users/',
        blank=True,
        null=True,
        default=None
    )
    is_admin = models.BooleanField(
        verbose_name='Права администратора',
        default=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_admin = True
            self.is_staff = True
        if self.is_admin:
            self.is_staff = True
        if not self.is_admin:
            self.is_staff = False
        super().save(*args, **kwargs)


class Subscription(models.Model):
    """Модель подписок."""

    subscriber = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='подписчик',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        default_related_name = 'subscriptions'
        ordering = ('author',)
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='unique_subscriber_author',
            )
        ]
