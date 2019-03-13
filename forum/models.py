from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import User


class Forum(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.CharField(max_length=10000)
	date = models.DateTimeField(auto_now_add=True)
	photo = models.FileField(upload_to='forum_photoes',blank=True , null=True)

	def __str__(self):
		return self.post

class ForumComment(models.Model):
	user = models.ForeignKey(User , on_delete=models.CASCADE)
	forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
	comment = models.CharField(max_length=500)
	comment_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.comment
