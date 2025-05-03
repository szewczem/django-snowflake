from django.conf import settings
from .image_config import IMAGE_PATHS

def global_image_paths(request):
    image_urls = {}

    for key, cloudinary_url in IMAGE_PATHS.items():
        if settings.DEBUG:
            # Strip the Cloudinary prefix to get the local path
            relative_path = cloudinary_url[76:]  # adjust if needed
            image_urls[key] = f"{settings.MEDIA_URL}{relative_path}"
        else:
            image_urls[key] = cloudinary_url

    return image_urls