import random
from django.core.management.base import BaseCommand
from reservations.models import Category, Equipment

categories = [
  'Ski',
  'Snowboard',
]

length = [
    '130',
    '145',
    '150',
    '165',
    '175',
]

level = [
    'begginer',
    'intermediate',
    'expert',
]

def generate_category():
    index = random.randint(0,1)
    return categories[index]

def generate_length():
    index = random.randint(0,4)
    return length[index]

def generate_level():
    index = random.randint(0,2)
    return level[index]


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help='The txt file that contains equipment names')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}.txt') as file:
            for row in file:
                name = row
                category_name = generate_category()
                length = generate_length()
                level = generate_level()

                category = Category.objects.get_or_create(name=category_name)

                equipment = Equipment(
                    category=Category.objects.get(name=category_name),
                    name=name,
                    length=length,
                    level=level,
                )
                equipment.save()     

        self.stdout.write(self.style.SUCCESS('Data created successfully'))