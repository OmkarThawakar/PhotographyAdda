from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from accounts.models import Album,Photo,UserProfile,RandomPhoto,RandomPhotoComment,AlbumComment


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'password'
        )

class MyProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'about',
            'place',
            'website',
            'skills',
            'phone',
            'image',
                       
        ) 

        def clean_data(self, commit=True):
            user = super(MyProfileForm, self).save(commit=False)
            user.about = self.cleaned_data['about']
            user.place = self.cleaned_data['place']
            user.website = self.cleaned_data['website']
            user.skills = self.cleaned_data['skills']
            user.phone = self.cleaned_data['phone']
            user.image = self.cleaned_data['image']
            
            if commit:
                user.save()

            return user

        
class CreateAlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ('photographer','album_title','album_logo')


class UploadPhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('about_photo','file')


class RandomPhotoForm(forms.ModelForm):

    class Meta:
        model = RandomPhoto
        fields = ('say_something','photo_file')



class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'fa fa-tag prefix grey-text'})
    )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "What do you want to say?"

class RandomPhotoCommentForm(forms.ModelForm):
    class Meta:
        model = RandomPhotoComment
        fields = ('body',)

class AlbumCommentForm(forms.ModelForm):
    class Meta:
        model = AlbumComment
        fields = ('comment_body',)







