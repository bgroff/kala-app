import errno
import os

from django.conf import settings


class AvatarUploader():
    def upload_avatar(self, file, user):
        filename = '{0}/{1}'.format(settings.AVATAR_BASE_PATH, user.uuid)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(filename, 'wb') as _file :
            _file.write(file.read())
            _file.close()
            user.avatar_url = '{0}/{1}'.format(settings.AVATAR_BASE_URL, user.uuid)
            user.save()
