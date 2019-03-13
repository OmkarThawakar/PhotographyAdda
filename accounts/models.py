from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	about = models.CharField(max_length=1000, default='')
	place = models.CharField(max_length=50,default='')
	website = models.URLField(default='')
	skills = models.CharField(max_length=1000)
	phone = models.IntegerField(default=0)
	image = models.FileField(upload_to='profile_image',blank=True)


	def __str__(self):
		return self.user.username

def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

class Album(models.Model):
	user = models.ForeignKey(User, default=1)
	photographer = models.CharField(max_length=250)
	album_title = models.CharField(max_length=100)
	album_logo = models.ImageField(upload_to='album_logo')
	album_added = models.DateTimeField(auto_now=True)
	is_favorite = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'album'
		verbose_name_plural = 'albums'

	def __str__(self):
		return self.album_title + ' - ' + self.photographer


class Photo(models.Model):
	album = models.ForeignKey(Album, on_delete=models.CASCADE)
	about_photo = models.CharField(max_length=1000 , blank=True , null=True)
	file = models.FileField(upload_to='photoes',blank=True)

	def __str__(self):
		return self.about_photo

class RandomPhoto(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	say_something = models.CharField(max_length=1000 , blank=True , null=True)
	randomphoto_added = models.DateTimeField(auto_now_add=True)
	photo_file = models.FileField(upload_to='my_photoes',blank=True)

	def __str__(self):
		return self.say_something

class RandomPhotoComment(models.Model):
	user = models.ForeignKey(User , on_delete=models.CASCADE)
	randomphoto = models.ForeignKey(RandomPhoto, on_delete=models.CASCADE)
	body = models.CharField(max_length=500)
	pub_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.body


class AlbumComment(models.Model):
	user = models.ForeignKey(User , on_delete=models.CASCADE)
	album = models.ForeignKey(Album, on_delete=models.CASCADE)
	comment_body = models.CharField(max_length=500)
	pub_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.comment_body




	

