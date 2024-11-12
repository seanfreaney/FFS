from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

print("Loading custom_storages.py")

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    default_acl = 'public-read'
    file_overwrite = True
    print(f"StaticStorage initialized with location: {location}")

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    default_acl = 'public-read'
    file_overwrite = True
    print(f"MediaStorage initialized with location: {location}")