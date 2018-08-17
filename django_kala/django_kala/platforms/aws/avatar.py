import boto3
from django.conf import settings


class AvatarUploader():
    def upload_avatar(self, file, user):
        client = boto3.client('s3')
        client.put_object(
            ACL='public-read',
            Body=file.read(),
            Key='avatars/{0}.png'.format(user.uuid),
            Bucket=settings.S3_STORAGE_BUCKET
        )

        user.avatar_url = 'https://s3-{0}.amazonaws.com/{1}/avatars/{2}.png'.format(
            settings.AWS_REGION,
            settings.S3_STORAGE_BUCKET,
            user.uuid
        )
        user.save()
