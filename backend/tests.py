from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


User = get_user_model()


class FoodgramAPITestCase(TestCase):
    def setUp(self):
        self.guest_client = APIClient()
        self.auth_client = APIClient()
        self.user = User.objects.create_user(username='auth_user')
        self.auth_client.force_authenticate(user=self.user)

    def test_auth_recipes_exists(self):
        """Проверка доступности списка рецептов."""
        response = self.auth_client.get('/api/recipes/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_guest_recipes_exists(self):
        """Проверка доступности списка рецептов."""
        response = self.guest_client.get('/api/recipes/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_auth_ingredients_exists(self):
        """Проверка доступности списка ингредиентов."""
        response = self.auth_client.get('/api/ingredients/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_guest_ingredients_exists(self):
        """Проверка доступности списка ингредиентов."""
        response = self.guest_client.get('/api/ingredients/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_auth_users_exists(self):
        """Проверка доступности списка пользователей."""
        response = self.auth_client.get('/api/users/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_guest_users_exists(self):
        """Проверка доступности списка пользователей."""
        response = self.guest_client.get('/api/users/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
