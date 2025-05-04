import os
import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.conf import settings

CLOUDINARY_BASE_FOLDER = 'descriptions'
DESCRIPTION_SUBFOLDERS = ['ski', 'snowboard', 'sled']
EXTENSION = '.txt'

class Command(BaseCommand):
    help = 'Uploads description txt files to Cloudinary'

    def handle(self, *args, **options):
        for sub in DESCRIPTION_SUBFOLDERS:
            local_dir = os.path.join(settings.BASE_DIR, 'media', 'equipment_description', sub)
            if not os.path.isdir(local_dir):
                self.stderr.write(f"Missing folder: {local_dir}")
                continue

            for fname in os.listdir(local_dir):
                if not fname.endswith(EXTENSION):
                    continue

                path = os.path.join(local_dir, fname)
                public_id = f"{CLOUDINARY_BASE_FOLDER}/{sub}/{os.path.splitext(fname)[0]}"
                
                try:
                    result = cloudinary.uploader.upload(
                        path,
                        public_id=public_id,
                        resource_type='raw',
                        overwrite=True
                    )
                    self.stdout.write(f"Uploaded: {result['secure_url']}")
                except Exception as e:
                    self.stderr.write(f"Upload failed for {path}: {e}")
            