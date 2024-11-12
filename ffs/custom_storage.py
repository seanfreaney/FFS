from storages.backends.s3boto3 import S3Boto3Storage
import logging

logger = logging.getLogger(__name__)

class StaticStorage(S3Boto3Storage):
    bucket_name = 'ffs-freaney-financial-services'
    location = 'static'
    file_overwrite = True
    default_acl = 'public-read'

    def _save(self, name, content):
        try:
            logger.error(f"Attempting to save {name} to S3")
            result = super()._save(name, content)
            logger.error(f"Successfully saved {name} to S3")
            return result
        except Exception as e:
            logger.error(f"Error saving {name} to S3: {str(e)}")
            raise
