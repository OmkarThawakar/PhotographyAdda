from django.contrib import admin
from accounts.models import UserProfile,Album,Photo,RandomPhoto,RandomPhotoComment,AlbumComment

admin.site.register(UserProfile)
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(RandomPhoto)
admin.site.register(RandomPhotoComment)
admin.site.register(AlbumComment)

def queryset(self, request):
    qs = super(UserProfile, self).queryset(request)
    return qs.only( about,place,website,skills,phone,image ) 
