from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    bucket_name = 'ffs-freaney-financial-services'
    location = 'static'
    file_overwrite = True
    default_acl = 'public-read'
