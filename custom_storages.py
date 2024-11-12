from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)  # Set to ERROR to ensure visibility

logger.error("CUSTOM_STORAGES: Module loaded")

class StaticStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        logger.error("CUSTOM_STORAGES: StaticStorage initialized")
        self.location = settings.STATICFILES_LOCATION
        self.default_acl = 'public-read'
        super().__init__(*args, **kwargs)
        logger.error(f"CUSTOM_STORAGES: StaticStorage location = {self.location}")

class MediaStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        logger.error("CUSTOM_STORAGES: MediaStorage initialized")
        self.location = settings.MEDIAFILES_LOCATION
        self.default_acl = 'public-read'
        super().__init__(*args, **kwargs)
        logger.error(f"CUSTOM_STORAGES: MediaStorage location = {self.location}")