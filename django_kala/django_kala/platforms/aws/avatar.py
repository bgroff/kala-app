import boto3
from django.conf import settings


class AvatarUploader():
    def get_s3_client(self):
        config = {
            'region_name': settings.KALA_STORAGE_REGION,
        }

        if settings.KALA_STORAGE_ENDPOINT:
            config['endpoint_url'] = settings.KALA_STORAGE_ENDPOINT

        if settings.KALA_STORAGE_AUTHENTICATION_TYPE == 'credentials':
            config['aws_access_key_id'] = settings.KALA_STORAGE_ACCESS_KEY
            config['aws_secret_access_key'] = settings.KALA_STORAGE_SECRET_KEY

        return boto3.client('s3', **config)

    def upload_avatar(self, file, user):
        self.get_s3_client().put_object(
            ACL='public-read',
            Body=file.read(),
            Key='{0}/avatars/{1}.png'.format(settings.KALA_STORAGE_BUCKET, user.uuid),
            Bucket=settings.S3_STORAGE_BUCKET
        )

        user.avatar_url = 'https://{0}.s3-{1}.amazonaws.com/{2}/avatars/{3}.png'.format(
            settings.KALA_STORAGE_BUCKET,
            'us-west-2',#settings.AWS_REGION,
            settings.KALA_STORAGE_PREFIX,
            user.uuid
        )
        user.save()
