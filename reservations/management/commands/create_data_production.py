import random
from django.core.management.base import BaseCommand
from reservations.models import Category, Equipment

from first_snowflake.image_config import IMAGE_PATHS


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
        key = f'EQUIPMENT_PHOTO_SKI_{index}'
    elif category_name=='Snowboard':
        index = random.randint(0,41)
        key = f'EQUIPMENT_PHOTO_SNOWBOARD_{index}'
    elif category_name=='Sled':
        index = random.randint(0,7)
        key = f'EQUIPMENT_PHOTO_SLED_{index}'
    else:
        key = 'EQUIPMENT_PHOTO_TEST'
    return IMAGE_PATHS.get(key, IMAGE_PATHS['EQUIPMENT_PHOTO_TEST'])
    

CLOUDINARY_DESCRIPTION_BASE = "https://res.cloudinary.com/defosob6j/raw/upload/descriptions"

def generate_description(category_name):
    if category_name=='Ski':
        index = random.randint(0,26)
        with open(f'{CLOUDINARY_DESCRIPTION_BASE}/ski/{index}.txt', 'r') as description_file:
            return description_file.read()
    elif category_name=='Snowboard':
        index = random.randint(0,19)
        with open(f'{CLOUDINARY_DESCRIPTION_BASE}/snowboard/{index}.txt', 'r') as description_file:
            return description_file.read()
    elif category_name=='Sled':
        index = random.randint(0,9)
        with open(f'{CLOUDINARY_DESCRIPTION_BASE}/sled/{index}.txt', 'r') as description_file:
            return description_file.read()
    else:
        with open(f'{CLOUDINARY_DESCRIPTION_BASE}/ski/test.txt', 'r') as description_file:
            return description_file.read()

class Command(BaseCommand):
    help = 'Generates equipment data and uploads images to Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help='The txt filename that contains equipment names')

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