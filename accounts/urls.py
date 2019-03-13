from django.contrib.auth.views import  (login,logout,
                                        password_reset,
                                        password_reset_done,
                                        password_reset_confirm,
                                        password_reset_complete,
                                       )

from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap

from .sitemaps import StaticViewSitemap
from . import views

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    #accounts/home
    url(r'^$', views.home , name='home'),

    #accounts/home
    url(r'^search/$', views.search , name='search'),

    #accounts/login
    url(r'^login/$',login , {'template_name':'accounts/login.html'}, name='login'),
    #accounts/logout
    url(r'^logout/$',logout , {'template_name':'accounts/logout.html'}, name='logout'),
    #accounts/register
    url(r'^register/$', views.register, name='register'),
    #accounts/profile
    url(r'^profile/$',views.view_profile , name='view_profile'),
    #accounts/profile/edit
    url(r'^profile/edit/$',views.edit_profile,name='edit_profile'),
    #accounts/change_password
    url(r'^change_password/$', views.change_password, name='change_password'),

    #accounts/profile/edit/my_profile
    url(r'^profile/edit/my_profile$',views.MyProfileFormView.as_view(),name='my_profile'),

    #accounts/reset_password
    url(r'^reset_password/$', password_reset,{'template_name':'accounts/reset_password.html',
     'post_reset_redirect':'accounts:password_reset_done',
     'email_template_name':'accounts/password_reset_email.html'},
      name='reset_password'),

    #accounts/reset_password/done
    url(r'^reset_password/done/$', password_reset_done,
     {'template_name':'accounts/password_reset_done.html'},
     name='password_reset_done'),

    #accounts/reset_password/confirm
    url(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
     password_reset_confirm,
     {'template_name':'accounts/password_reset_confirm.html','post_reset_redirect':'accounts:password_reset_complete'},
     name='password_reset_confirm'),

    #accounts/reset_password/confirm
    url(r'^reset_password/complete/$',
     password_reset_complete,{'template_name':'accounts/password_reset_complete.html'},
     name='password_reset_complete'),

    #accounts/create_album
    url(r'^create_album/$', views.create_album, name='create_album'),

    #accounts/upload_random_photo
    url(r'^random_photo/$', views.random_photo, name='random_photo'),

    #accounts/gallery
    url(r'^gallery/$',views.gallery,name='gallery'),

    #accounts/upload_photo
    url(r'^(?P<album_id>[0-9]+)/upload_photo/$',views.upload_photo,name='upload_photo'),

    #account/album/details
    url(r'^(?P<album_id>[0-9]+)/$', views.details, name='details'),

    #accounts/delete_album
    url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),

    #accounts/album/details/delete_photo
    url(r'^(?P<album_id>[0-9]+)/delete_photo/(?P<photo_id>[0-9]+)/$', views.delete_photo, name='delete_photo'),

    #accounts/delete_random_photo
    url(r'^(?P<randomphoto_id>[0-9]+)/delete_random_photo/$', views.delete_random_photo, name='delete_random_photo'),

    #accounts/randomphoto/add_comment
    url(r'^(?P<randomphoto_id>[0-9]+)/add_comment/$',views.randomphoto_comment,name='randomphoto_comment'),

    #accounts/album/add_comment
    url(r'^(?P<album_id>[0-9]+)/album_comment/$',views.album_comment,name='album_comment'),

    #accounts/about
    url(r'^about/$', views.about, name='about'),

    #accounts/contact
    url(r'^contact/$', views.contact, name='contact'),

    #accounts/photo_set
    url(r'^photo_set/$', views.photo_set, name='photo_set'),

    #accounts/my_gallery
    url(r'^randomphotoes/$', views.randomphotoes, name='randomphotoes'),

    #accounts/my_uploads
    url(r'^(?P<user_id>[0-9]+)/my_uploads/$', views.my_uploads, name='my_uploads'),

    #accounts/my_albums
    url(r'^(?P<user_id>[0-9]+)/my_albums/$', views.my_albums, name='my_albums'),

    #account/album/album_set
    url(r'^(?P<album_id>[0-9]+)/album_set$', views.album_set, name='album_set'),

    #accounts/photographers
    url(r'^photographers/$', views.photographers, name='photographers'),

    #accounts/sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),


]
