from django import forms


class AvatarForm(forms.Form):
    avatar = forms.FileField()
