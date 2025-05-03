import os
import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.conf import settings

# Folders under your project-level media/ directory:
MEDIA_SUBFOLDERS = ['footer', 'home', 'register', 'equipment_photo',]
# The folder prefix in your Cloudinary account:
CLOUDINARY_BASE_FOLDER = 'static_images'

class Command(BaseCommand):
    help = 'Uploads media/... images to Cloudinary and writes image_config.py'

    def handle(self, *args, **options):
        image_urls = {}

        # Loop through each subfolder under <project_root>/media/
        for sub in MEDIA_SUBFOLDERS:
            local_dir = os.path.join(settings.BASE_DIR, 'media', sub)
            if not os.path.isdir(local_dir):
                self.stdout.write(self.style.WARNING(f"Skipped missing folder: {local_dir}"))
                continue

            for fname in os.listdir(local_dir):
                if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.svg', '.webp')):
                    continue

                local_path = os.path.join(local_dir, fname)
                public_id = f"{CLOUDINARY_BASE_FOLDER}/{sub}/{os.path.splitext(fname)[0]}"
                self.stdout.write(f"Uploading {local_path} → Cloudinary as {public_id} ...")

                try:
                    result = cloudinary.uploader.upload(
                        local_path,
                        public_id=public_id,
                        overwrite=True,
                        resource_type='image'
                    )
                    key = f"{sub.upper()}_{os.path.splitext(fname)[0].upper()}"
                    image_urls[key] = result['secure_url']
                except Exception as e:
                    self.stderr.write(f"Failed to upload {local_path}: {e}")

        # Write the config file into your project package (alongside settings.py)
        config_dir = os.path.join(settings.BASE_DIR, settings.ROOT_URLCONF.split('.')[0])
        os.makedirs(config_dir, exist_ok=True)
        cfg_path = os.path.join(config_dir, 'image_config.py')

        with open(cfg_path, 'w') as cfg:
            cfg.write("IMAGE_PATHS = {\n")
            for key, url in image_urls.items():
                cfg.write(f"    '{key}': '{url}',\n")
            cfg.write("}\n")

        self.stdout.write(self.style.SUCCESS(
            f"Uploaded {len(image_urls)} images and updated {cfg_path}"
        ))