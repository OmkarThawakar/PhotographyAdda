from django import forms
from django.contrib.auth.models import User
from forum.models import Forum,ForumComment

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ('post','photo',)

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ('comment',)

