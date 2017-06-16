from django import forms
from django.contrib.auth.models import User

from .models import Album, Photo


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = [ 'photographer', 'album_title', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['name', 'file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
