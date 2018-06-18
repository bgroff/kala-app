from django.conf import settings
from uuid import uuid4

import boto3


class DocumentHandler():

    def get_document_url(self, document):
        s3 = boto3.client('s3')
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': settings.S3_STORAGE_BUCKET,
                'Key': 'media/documents/"{0}"'.format(document.uuid),
                'ResponseContentDisposition': 'attachment; filename={0}'.format(document.name),
            }
        )
        return url

    def upload_document(self, content, key):
        s3 = boto3.client('s3')
        s3.put_object(
            ACL='private',
            Body=content,
            Bucket=settings.S3_STORAGE_BUCKET,
            Key='media/documents/{0}'.format(key),
            ServerSideEncryption='AES256'
        )

    def upload_export(self, export_path):
        key = 'exports/{0}'.format(uuid4())

        s3 = boto3.client('s3')
        s3.meta.client.upload_file(
            export_path,
            settings.S3_STORAGE_BUCKET,
            key
        )

        return {'Key': key}

    def archive_document(self, document):
        raise NotImplementedError()

    def retrieve_document(self, document):
        raise NotImplementedError()
