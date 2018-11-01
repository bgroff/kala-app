import errno
import os
from uuid import uuid4

from django.conf import settings

import shutil


class DocumentHandler():

    def get_document_url(self, document):
        return '{0}/{1}'.format(settings.DOCUMENT_BASE_URL, document.uuid)

    def upload_document(self, content, key):
        filename = '{0}/{1}'.format(settings.DOCUMENT_BASE_PATH, key)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(filename, 'wb') as _file :
            _file.write(content)
            _file.close()

    def upload_export(self, export_path):
        filename = '{0}/{1}'.format(settings.EXPORT_BASE_PATH, key)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        key = '{0}'.format(uuid4())

        shutil.move(
            export_path,
            filename
        )

        return {'Key', key}

    def get_export_url(self, export):
        return '{0}/{1}'.format(settings.EXPORT_BASE_URL, export.details['Key'])

    def archive_document(self, document):
        pass

    def retrieve_document(self, document):
        pass
