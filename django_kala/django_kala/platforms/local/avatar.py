from django.conf import settings
import tempfile
import os


class AvatarUploader():
    def upload_avatar(self, file, user):
        _file, _path = tempfile.mkstemp()
        os.write(_file, file.read())
        user.avatar_url = settings.AVATAR_BASE_URL + _path.split('/')[-1]
        user.save()
