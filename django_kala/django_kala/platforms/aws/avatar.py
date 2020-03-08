import boto3
from django.conf import settings


class AvatarUploader():
    def upload_avatar(self, file, user):
        client = boto3.client('s3')
        client.put_object(
            ACL='public-read',
            Body=file.read(),
            Key='{0}/avatars/{1}.png'.format(settings.S3_STORAGE_PREFIX, user.uuid),
            Bucket=settings.S3_STORAGE_BUCKET
        )

        user.avatar_url = 'https://{0}.s3-{1}.amazonaws.com/{2}/avatars/{3}.png'.format(
            settings.S3_STORAGE_BUCKET,
            'us-west-2',#settings.AWS_REGION,
            settings.S3_STORAGE_PREFIX,
            user.uuid
        )
        user.save()
