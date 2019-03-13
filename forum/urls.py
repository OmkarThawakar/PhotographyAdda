from django.conf.urls import url
from . import views
from accounts import views as default_views

urlpatterns = [
    #forum/home
    url(r'^$', views.forums , name='forums'),

    #forum/create_post
    url(r'^create_post/$', views.create_post , name='create_post'),

    #forum/delete_post
    url(r'^(?P<post_id>[0-9]+)/delete_post/$', views.delete_post, name='delete_post'),

    #forum/post_comment
    url(r'^(?P<post_id>[0-9]+)/post_comment/$', views.post_comment, name='post_comment'),


 ]




 