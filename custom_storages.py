from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import logging

logger = logging.getLogger(__name__)

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    
    def __init__(self, *args, **kwargs):
        print("StaticStorage initialized")  # Debug print
        super().__init__(*args, **kwargs)
    
    def _save(self, name, content):
        print(f"Attempting to save {name} to S3")  # Debug print
        try:
            result = super()._save(name, content)
            print(f"Successfully saved {name} to S3")
            return result
        except Exception as e:
            print(f"Error saving to S3: {str(e)}")
            raise

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION