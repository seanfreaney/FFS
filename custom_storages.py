from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

print("Loading custom_storages.py")
print(f"STATICFILES_LOCATION: {settings.STATICFILES_LOCATION}")
print(f"STATIC_URL: {settings.STATIC_URL}")

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    print(f"StaticStorage location: {location}")


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION