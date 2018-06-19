from io import BytesIO

from django import forms
from PIL import Image


class AvatarForm(forms.Form):
    avatar = forms.FileField()

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        try:
            image = Image.open(BytesIO(avatar.read()))
        except:
            raise forms.ValidationError('The image provided was not readable')
        if not image.format == 'JPEG' and not image.format == 'PNG' and not image.format == 'GIF':
            raise forms.ValidationError('The image must be a JPEG, PNG or GIF, found {0}'.format(image.format))

        return avatar.seek(0)
