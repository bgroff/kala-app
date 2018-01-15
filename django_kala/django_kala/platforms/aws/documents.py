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
                'Key': 'media/{0}'.format(document.file.name)
            }
        )

    def upload_project_export(self, export_path):
        key = 'exports/{0}'.format(uuid4())

        s3 = boto3.client('s3')
        s3.meta.client.upload_file(
            export_path,
            settings.S3_STORAGE_BUCKET,
            key
        )

        return {'Key': key}
