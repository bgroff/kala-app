from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _

from documents.models import Document
from projects.models import Export

import os
import requests
import tempfile
import shutil

User = get_user_model()


class ExportDocumentTask():

    def run(self, *args, **kwargs):
        document = Document.objects.get(pk=args[0])
        user = User.objects.get(pk=args[1])
        manager = settings.PLATFORM_MANAGER()

        # If the user does not have change or create priviliages, fail.
        if not document.can_create(user):
            # TODO: this should be logged
            return False

        # Create a temp dir and documents directory inside.
        path = tempfile.mkdtemp()
        os.mkdir(path + '/documents')

        # Save the path on the task for later cleanup
        self.path = path

        # TODO: If the file exists, we should append a unique id so that
        # the files do not overwrite each other.
        # Download all the documents into the documents dir.
        for version in document.documentversion_set.all():
            response = requests.get(manager.get_document_url(version), stream=True)
            with open('{0}/{1}/{2}'.format(path, 'documents', version.name), 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)

        # Make a zip file from all the documents
        export_path = shutil.make_archive(
            '{0}/{1}'.format(path, document.name),
            'zip',
            '{0}/{1}'.format(path, '/documents')
        )

        # Upload the document somewhere.
        export_details = manager.upload_export(export_path)
        export = Export.objects.create(
            name=export_path.split('/')[-1],
            user=user,
            details=export_details,
            key=get_random_string(length=78)
        )

        # Cleanup the temp files.
        self.cleanup()

        # TODO: this will need to be refactored when a notification is in place.
        # Send a notification to download
        user.send_invite(
            settings.EMAIL_APP,
            'email/document_export',
            _('Document Export'),
            export
        )

    def cleanup(self):
        shutil.rmtree(self.path)
