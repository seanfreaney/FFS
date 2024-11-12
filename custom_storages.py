from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import logging

logger = logging.getLogger(__name__)

logger.error("Loading custom_storages.py")

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    logger.error(f"StaticStorage initialized with location: {location}")

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    logger.error(f"MediaStorage initialized with location: {location}")