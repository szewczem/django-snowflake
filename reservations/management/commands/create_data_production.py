import random
from django.core.management.base import BaseCommand
from reservations.models import Category, Equipment

from first_snowflake.image_config import IMAGE_PATHS
import requests
from urllib.request import urlopen
from django.core.files import File
from tempfile import NamedTemporaryFile


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

def generate_banner_url(category_name):
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
        url = f'{CLOUDINARY_DESCRIPTION_BASE}/ski/{index}.txt'
    elif category_name=='Snowboard':
        index = random.randint(0,19)
        url = f'{CLOUDINARY_DESCRIPTION_BASE}/snowboard/{index}.txt'
    elif category_name=='Sled':
        index = random.randint(0,9)
        url = f'{CLOUDINARY_DESCRIPTION_BASE}/sled/{index}.txt'
    else:
        url = f'{CLOUDINARY_DESCRIPTION_BASE}/ski/test.txt'
        
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Failed to fetch description from {url}: {e}")
        return "No description available."

class Command(BaseCommand):
    help = 'Generates equipment data and uploads images to Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help='The txt filename that contains equipment names')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        try:
            with open(f"{file_name}.txt") as f:
                names = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.stderr.write(f"File {file_name}.txt not found")
            return

        created = 0
        for name in names:
            category_name = generate_category()
            length = generate_length()
            level = generate_level()
            banner_url = generate_banner_url(category_name)
            description = generate_description(category_name)

            category, _ = Category.objects.get_or_create(name=category_name)

            equipment = Equipment(
                category=category,
                name=name, 
                length=length,
                level=level,
                banner=banner_url,
                description=description,
            )
            try:
                equipment.save()
                created += 1
                self.stdout.write(f"Created: {equipment.name}")
            except Exception as e:
                self.stderr.write(f"Failed to create {name}: {e}")

        self.stdout.write(self.style.SUCCESS(f"Done! Created {created} equipment entries."))