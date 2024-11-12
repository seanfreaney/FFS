from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import logging
import boto3

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    
    def __init__(self, *args, **kwargs):
        print("StaticStorage: Initializing...")
        print(f"StaticStorage: Location = {settings.STATICFILES_LOCATION}")
        print(f"StaticStorage: Bucket = {settings.AWS_STORAGE_BUCKET_NAME}")
        super().__init__(*args, **kwargs)

    def _save(self, name, content):
        print(f"StaticStorage: Attempting to save {name}")
        try:
            # Test S3 connection
            s3 = boto3.client('s3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            print("StaticStorage: S3 client created successfully")
            
            result = super()._save(name, content)
            print(f"StaticStorage: Successfully saved {name}")
            return result
        except Exception as e:
            print(f"StaticStorage: Error saving {name}: {str(e)}")
            raise

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION