from django.conf import settings

import shutil



class DocumentHandler():

    def get_document_url(self, document):
        return '{0}/media/documents/{1}'.format('http://localhost', document.file.name)

    def upload_export(self, export_path):
        shutil.move(
            export_path,
            '{0}/{1}'.format(settings.EXPORT_DIRECTORY, export_path.split('/')[-1])
        )

        return {}
