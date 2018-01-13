import boto3
from django.conf import settings


class AvatarUploader():
    def upload_avatar(self, file, user):
        client = boto3.client('s3')
        client.put_object(
            ACL='public-read',
            Body=file.read(),
            Key='avatars/{0}.png'.format(user.uuid),
            Bucket=settings.S3_MEDIA_URL
        )
        user.avatar_url = 'https://s3-us-west-2.amazonaws.com/ndptc-kala/avatars/{0}.png'.format()
