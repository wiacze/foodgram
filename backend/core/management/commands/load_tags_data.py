import csv
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from foodgram_backend.settings import CSV_DATA_DIR
from core.models import Tag


class Command(BaseCommand):
    help = 'Import CSV data to a Django model'

    def handle(self, *args, **kwargs):
        with open(
            f'{CSV_DATA_DIR}/tags.csv', encoding='utf-8'
        ) as file:
            try:
                reader = csv.reader(file)
                tags = [
                    Tag(
                        name=row[0],
                        slug=row[1],
                    )
                    for row in reader
                ]
                Tag.objects.bulk_create(tags)
                self.stdout.write(
                    self.style.SUCCESS('Tags added successfully!')
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR('Tags already exists!')
                )
