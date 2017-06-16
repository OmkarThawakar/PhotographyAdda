from django.conf.urls import url
from . import views

app_name = 'photoapp'

urlpatterns = [
    #photoapp/
    url(r'^$', views.index, name='index'),
    #register/
    url(r'^register/$', views.register, name='register'),
    #login_user/
    url(r'^login_user/$', views.login_user, name='login_user'),
    #logout_user/
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    #photoapp/album/
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    #photoapp/album/<song_favourite>/
    url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    #photoapp/search/
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    #photoapp/create_album/
    url(r'^create_album/$', views.create_album, name='create_album'),
    #photoapp/<album_id>/create_song/
    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    #photoapp/<album_id>/delete_song/<song_id>/
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    #photoapp/albums/<is_favourite>/
    url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
    #photoapp/albums/<delete_album>/
    url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
    #photoappcontact
    url(r'^contact/$',views.contact,name='contact'),
]
