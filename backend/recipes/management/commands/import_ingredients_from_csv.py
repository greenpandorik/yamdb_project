import csv, os, time

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных из csv в БД ингридиенты'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        i = 0
        print('Заполнение БД ингридиенты из csv успешно запущено.')
        file_path = options['path'] + 'ingredients.csv'
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                i = i + 1
                try:
                    obj, created = Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
                    if not created:
                        print(
                            f'Ингредиент {obj} уже существует в базе данных.'
                        )
                except Exception as error:
                    print(f'Ошибка в строке {row}: {error}')
        print(f'Перенесено {i} строк')
        print('Заполнение БД ингридиентов успешно завершено. 👌')
