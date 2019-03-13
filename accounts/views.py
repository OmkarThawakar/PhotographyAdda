from django.shortcuts import render,redirect,get_object_or_404
from accounts.forms import (RegistrationForm,
                            EditProfileForm,
                            CreateAlbumForm,
                            UploadPhotoForm,
                            MyProfileForm,
                            RandomPhotoForm,
                            ContactForm,
                            RandomPhotoCommentForm,
                            AlbumCommentForm
                            )
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import Album,Photo,RandomPhoto,UserProfile,RandomPhotoComment,AlbumComment
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.db import transaction
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views import generic
from django.views.generic import View

from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

from django.contrib.auth.models import User


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def search(request):
    randomphotoes = RandomPhoto.objects.all()
    albums = Album.objects.all()
    comments = RandomPhotoComment.objects.all()
    album_comments = AlbumComment.objects.all()
    photographers = UserProfile.objects.all()
    users = User.objects.all()
    query = request.GET.get("q")
    if query :
        randomphotoes = randomphotoes.filter(
            Q(say_something__icontains=query)
        ).distinct()
        albums = albums.filter(
            Q(album_title__icontains=query)|
            Q(photographer__icontains=query)
        ).distinct()
        photographers = photographers.filter(
            Q(about__icontains=query)|
            Q(skills__icontains=query)|
            Q(place__icontains=query)
        ).distinct()
        users = users.filter(
            Q(first_name__icontains=query)|
            Q(last_name__icontains=query)
        ).distinct()
        return render(request,'accounts/search.html',{
            'randomphotoes':randomphotoes,
            'albums':albums,
            'comments':comments,
            'album_comments':album_comments,
            'photographers':photographers,
            'users':users
            })
    else:
        return render(request, 'accounts/search.html',{'photoes':randomphotoes,'comments':comments})

def home(request):
    album_list = Album.objects.all()[::-1]
    photo_list = RandomPhoto.objects.all().order_by('-randomphoto_added')
    photographer_list = UserProfile.objects.all()[::-1]
    comments = RandomPhotoComment.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(photo_list, 8)
    album_paginator = Paginator(album_list,6)
    photographer_paginator = Paginator(photographer_list , 6)
    try:
        photoes = paginator.page(page)
        albums = album_paginator.page(page)
        photographers = photographer_paginator.page(page)
    except PageNotAnInteger:
        photoes = paginator.page(1)
        albums = album_paginator.page(1)
        photographers = photographer_paginator.page(1)
    except EmptyPage:
        photoes = paginator.page(paginator.num_pages)
        albums = album_paginator.page(album_paginator.num_pages)
        photographers = photographer_paginator.page(photographer_paginator.num_pages)
    args = {
        'photoes':photoes,
        'albums':albums,
        'comments':comments,
        'photographers':photographers

        }
    return render(request, 'accounts/home.html',args)

def register(request):
    if request.method=='POST' :
        form = RegistrationForm(request.POST)
        if form.is_valid() :
            form.save()
            return redirect('/accounts')
        else:
            return redirect('/accounts/register')
    else:
        form = RegistrationForm()

        args = { 'form': form }
        return render(request, 'accounts/reg_form.html', args)

def view_profile(request):
    photo_list = RandomPhoto.objects.filter(user=request.user)
    album_list = Album.objects.filter(user=request.user)
    comments = RandomPhotoComment.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(photo_list, 8)
    album_paginator = Paginator(album_list,6)
    try:
        photoes = paginator.page(page)
        albums = album_paginator.page(page)
    except PageNotAnInteger:
        photoes = paginator.page(1)
        albums = album_paginator.page(1)
    except EmptyPage:
        photoes = paginator.page(paginator.num_pages)
        albums = album_paginator.page(album_paginator.num_pages)
    args = {
        'photoes':photoes,
        'comments':comments,
        'albums':albums

        }
    return render(request, 'accounts/profile.html',args)

def edit_profile(request):

    if request.method == 'POST' :
        user_form = EditProfileForm(request.POST , instance=request.user)
        if user_form.is_valid() :
            user_form.save()
            return redirect('/accounts/profile')
        else:
            return redirect('/account/edit_profile.html')
    else:
        user_form = EditProfileForm(instance=request.user)

        args = {
        'user_form':user_form
         }
        return render(request, 'accounts/edit_profile.html', args)

def change_password(request):

    if request.method == 'POST' :
        form = PasswordChangeForm(data=request.POST , user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts')
        else:
            return redirect('/accounts/change_password')

    else:
        form = PasswordChangeForm(user=request.user)

        args = { 'form':form }
        return render(request, 'accounts/change_password.html', args)

def random_photo(request):
    if not request.user.is_authenticated():
        return render(request, 'accounts/login.html')
    else:
        form = RandomPhotoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            my_photo = form.save(commit=False)
            my_photo.user = request.user
            my_photo.photo_file = request.FILES['photo_file']
            file_type = my_photo.photo_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'my_photo': my_photo,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'accounts/random_photo.html', context)

            my_photo.save()
            return redirect('accounts:home')

        context = {
            "form": form,
        }
        return render(request, 'accounts/random_photo.html', context)

def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'accounts/login.html')
    else:
        form = CreateAlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'accounts/create_album.html', context)

            album.save()
            return render(request, 'accounts/album_set.html', {'album': album})

        context = {
            "form": form,
        }
        return render(request, 'accounts/create_album.html', context)

def upload_photo(request, album_id):
    form = UploadPhotoForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_photoes = album.photo_set.all()
        for s in albums_photoes:
            if s.about_photo == form.cleaned_data.get("about_photo"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that photo',
                }
                return render(request, 'accounts/upload_photo.html', context)
        photo = form.save(commit=False)
        photo.album = album
        photo.file = request.FILES['file']
        file_type = photo.file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'accounts/upload_photo.html', context)

        photo.save()
        return render(request, 'accounts/album_set.html', {'album': album})

    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'accounts/upload_photo.html', context)

def gallery(request):
    album_list = Album.objects.all()
    comments = AlbumComment.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(album_list, 4)
    try:
        albums = paginator.page(page)
    except PageNotAnInteger :
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)
    return render(request, 'accounts/gallery.html', {'albums': albums , 'comments':comments})

def details(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'accounts/details.html', {'album': album, 'user': user})

def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    return render(request, 'accounts/gallery.html', {'albums': albums})

def delete_photo(request, album_id, photo_id):
    album = get_object_or_404(Album, pk=album_id)
    photo = Photo.objects.get(pk=photo_id)
    photo.delete()
    return render(request, 'accounts/album_set.html', {'album': album})

def delete_random_photo(request, randomphoto_id):
    random_photo = RandomPhoto.objects.get(pk=randomphoto_id)
    random_photo.delete()
    random_photoes = RandomPhoto.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'random_photoes': random_photoes})


class MyProfileFormView(View):
    form_class = MyProfileForm
    template_name = 'accounts/my_profile.html'

    #display blank form
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    #process form data
    def post(self,request):
        form = self.form_class(request.POST,request.FILES,instance=request.user.userprofile)
        if form.is_valid() :
            profile = form.save(commit=False)
            #cleaned (normalise) data
            profile.user = request.user
            about = form.cleaned_data['about']
            place = form.cleaned_data['place']
            website = form.cleaned_data['website']
            skills = form.cleaned_data['skills']
            phone = form.cleaned_data['phone']
            image = form.cleaned_data['image']

            profile.save()  #now user info is saved

            if profile is not None :
                return redirect('accounts:view_profile')

        return render(request,self.template_name,{'form':form})

def contact(request):
    form_class = ContactForm
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('accounts/contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "PhotographyAdda.com" +'',
                ['omee0805@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('accounts:contact')

    return render(request, 'accounts/contact.html', {
        'form': form_class,
    })

def randomphoto_comment(request, randomphoto_id):
    if not request.user.is_authenticated():
        return redirect('accounts:login')
    else:
        get_randomphoto = RandomPhoto.objects.get(id=randomphoto_id)
        if request.method == 'POST' :
            form = RandomPhotoCommentForm(request.POST or None)
            if form.is_valid() :
                mycomment = form.save(commit=False)
                body = form.cleaned_data['body']
                mycomment.randomphoto = get_randomphoto
                mycomment.user = request.user
                mycomment.save()
                print("\nform is valid!!!!\n")
                return redirect('accounts:home')
            else:
                print("\nform is not valid!!\n")
                return redirect('accounts:home')
        else:
            form = RandomPhotoCommentForm(request.POST or None)

            args = {
            'form':form
             }
            return render(request, 'accounts/home.html', args)

def album_comment(request, album_id):
    if not request.user.is_authenticated():
        return redirect('accounts:login')
    else:
        album = Album.objects.get(id=album_id)
        if request.method == 'POST' :
            form = AlbumCommentForm(request.POST or None)
            if form.is_valid() :
                album_comment = form.save(commit=False)
                comment_body = form.cleaned_data['comment_body']
                album_comment.album = album
                album_comment.user = request.user
                album_comment.save()
                print("\nform is valid!!!!\n")
                return redirect('accounts:gallery')
            else:
                print("\nform is not valid!!\n")
                return redirect('accounts:gallery')
        else:
            form = AlbumCommentForm(request.POST or None)

            args = {
            'form':form
             }
            return render(request, 'accounts/gallery.html', args)

def about(request):
    return render(request, 'accounts/about.html')


def photo_set(request):
    photo_list = RandomPhoto.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(photo_list, 8)
    try:
        photoes = paginator.page(page)
    except PageNotAnInteger:
        photoes = paginator.page(1)
    except EmptyPage:
        photoes = paginator.page(paginator.num_pages)

    return render(request, 'accounts/photoset.html', { 'photoes': photoes })


def album_set(request, album_id):
    user = request.user
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'accounts/album_set.html', {'album': album, 'user': user})


def randomphotoes(request):
    photo_list = RandomPhoto.objects.filter(user=request.user)
    comments = RandomPhotoComment.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(photo_list, 4)
    try:
        photoes = paginator.page(page)
    except PageNotAnInteger:
        photoes = paginator.page(1)
    except EmptyPage:
        photoes = paginator.page(paginator.num_pages)
    args = {
        'photoes':photoes,
        'comments':comments
    }
    return render(request,'accounts/randomphotoes.html',args)

def photographers(request):
    users = User.objects.all()[::-1]
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 9)
    try:
        photographers = paginator.page(page)
    except PageNotAnInteger :
        photographers = paginator.page(1)
    except EmptyPage:
        photographers = paginator.page(paginator.num_pages)
    return render(request, 'accounts/photographer.html',{'photographers':photographers})

def my_uploads(request , user_id):
    user = get_object_or_404(User, pk=user_id)
    photo_list = RandomPhoto.objects.filter(user = user)
    comments = RandomPhotoComment.objects.all()
    paginator = Paginator(photo_list, 2)
    page = request.GET.get('page', 1)
    try:
        photoes = paginator.page(page)
    except PageNotAnInteger:
        photoes = paginator.page(1)
    except EmptyPage:
        photoes = paginator.page(paginator.num_pages)
    args = {
        'photoes':photoes,
        'comments':comments,
        'user':user
    }
    return render(request,'accounts/my_randomphotoes.html',args)

def my_albums(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    album_list = Album.objects.filter(user=user)
    comments = AlbumComment.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(album_list, 4)
    print("paginator",paginator)
    try:
        albums = paginator.page(page)
    except PageNotAnInteger :
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)
    args = {
        'albums': albums ,
         'comments':comments,
         'user':user
         }
    return render(request, 'accounts/my_gallery.html', args)

