import random
from django.core.management.base import BaseCommand
from reservations.models import Category, Equipment

categories = [
  'Ski',
  'Ski',
  'Ski',
  'Ski',
  'Ski',
  'Ski',
  'Snowboard',
  'Snowboard',
  'Snowboard',
  'Sled',
]

length = [
    '130',
    '145',
    '150',
    '165',
    '170',
    '175',
    '180',
]

level = [
    'beginner',
    'intermediate',
    'advanced',
]

def generate_category():
    index = random.randint(0,9)
    return categories[index]

def generate_length():
    index = random.randint(0,4)
    return length[index]

def generate_level():
    index = random.randint(0,2)
    return level[index]

def generate_banner(category_name):
    if category_name=='Ski':
        index = random.randint(0,61)
        return f'equipment_photo/ski/{index}.jpg'
    elif category_name=='Snowboard':
        index = random.randint(0,41)
        return f'equipment_photo/snowboard/{index}.jpg'
    elif category_name=='Sled':
        index = random.randint(0,7)
        return f'equipment_photo/sled/{index}.jpg'
    else:
        return f'equipment_photo/test.jpg'
    
def generate_description(category_name):
    if category_name=='Ski':
        index = random.randint(0,26)
        with open(f'media/equipment_description/ski/{index}.txt', 'r') as description_file:
            return description_file.read()
    elif category_name=='Snowboard':
        index = random.randint(0,19)
        with open(f'media/equipment_description/snowboard/{index}.txt', 'r') as description_file:
            return description_file.read()
    elif category_name=='Sled':
        index = random.randint(0,9)
        with open(f'media/equipment_description/sled/{index}.txt', 'r') as description_file:
            return description_file.read()
    else:
        with open(f'media/equipment_description/ski/test.txt', 'r') as description_file:
            return description_file.read()

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
                banner = generate_banner(category_name)
                description = generate_description(category_name)

                category, _ = Category.objects.get_or_create(name=category_name)

                equipment = Equipment(
                    category=category,
                    name=name,
                    length=length,
                    level=level,
                    banner=banner,
                    description=description,
                )
                equipment.save()     

        self.stdout.write(self.style.SUCCESS('Data created successfully'))