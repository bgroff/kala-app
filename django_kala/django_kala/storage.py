from django.conf import settings


if not settings.DEBUG:
    from storages.backends.s3boto3 import S3Boto3Storage

    AWS_MEDIA_STORAGE_BUCKET = settings.S3_STORAGE_BUCKET
    MEDIA_URL = settings.S3_MEDIA_URL
    MEDIAFILES_LOCATION = 'media'


    class MediaStorage(S3Boto3Storage):
        location = MEDIAFILES_LOCATION
        custom_domain = MEDIA_URL.strip('/')
        bucket_name = AWS_MEDIA_STORAGE_BUCKET
        default_acl = 'private'
