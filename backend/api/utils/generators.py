import random
import string
from django.http import HttpResponse
from rest_framework import status

from foodgram_backend.constants import MIN_HASH_LENGTH, MAX_HASH_LENGTH


def generate_hash():
    length = random.randint(MIN_HASH_LENGTH, MAX_HASH_LENGTH)
    return (
        ''.join(random.sample(string.ascii_letters + string.digits, k=length))
    )


def generate_shopping_list(content: list):
    data = ['Список покупок:']
    count = 0
    for item in content:
        name = item['ingredient__name']
        amount = item['amount']
        measurement_unit = item['ingredient__measurement_unit']
        count += 1
        data.append(f'{count}. {name} - {amount} {measurement_unit}.')
    data = '\n'.join(data)
    return HttpResponse(
        data, status=status.HTTP_200_OK,
        headers={
            'Content-Type': 'text/plain,charset=utf8',
            'Content-Disposition': 'attachment; filename=shopping_list.txt'
        }
    )
