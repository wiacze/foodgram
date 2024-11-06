import csv
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from foodgram_backend.settings import CSV_DATA_DIR
from core.models import Ingredient


class Command(BaseCommand):
    help = 'Import CSV data to a Django model'

    def handle(self, *args, **kwargs):
        with open(
            f'{CSV_DATA_DIR}/ingredients.csv', encoding='utf-8'
        ) as file:
            try:
                reader = csv.reader(file)
                ingredients = [
                    Ingredient(
                        name=row[0],
                        measurement_unit=row[1],
                    )
                    for row in reader
                ]
                Ingredient.objects.bulk_create(ingredients)
                self.stdout.write(
                    self.style.SUCCESS('Ingredients added successfully!')
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR('Ingredients already exists!')
                )
