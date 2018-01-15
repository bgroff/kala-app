from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from projects.models import Project, Export

import celery
import os
import requests
import tempfile
import shutil

User = get_user_model()


class ExportProjectTask(celery.Task):

    def run(self, *args, **kwargs):
        project = Project.objects.get(pk=args[0])
        user = User.objects.get(pk=args[1])
        manager = settings.PLATFORM_MANAGER()

        # If the user does not have change or create priviliages, fail.
        if not project.has_change(user) and not project.has_create(user):
            # TODO: this should be logged
            return False

        # Create a temp dir and documents directory inside.
        path = tempfile.mkdtemp()
        os.mkdir(path + '/documents')

        # Save the path on the task for later cleanup
        self.path = path

        # Download all the documents into the documents dir.
        for document in project.get_documents(user):
            latest = document.get_latest()
            response = requests.get(manager.get_document_url(latest), stream=True)
            with open('{0}/{1}/{2}'.format(path, 'documents', latest.file.name), 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)

        # Make a zip file from all the documents
        export_path = shutil.make_archive(
            '{0}/{1}'.format(path, project.name),
            'zip',
            '{0}/{1}'.format(path, '/documents')
        )

        # Upload the document somewhere.
        export_details = manager.upload_project_export(export_path)
        export = Export.objects.create(
            user=user,
            details=export_details,
            key=get_random_string(length=255)
        )

        # Cleanup the temp files.
        self.cleanup()

    def cleanup(self):
        shutil.rmtree(self.path)
