from django.shortcuts import render , redirect
from forum.models import Forum , ForumComment
from forum.forms import ForumForm , ForumCommentForm

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def forums(request):
    posts = Forum.objects.all()[::-1]
    comments = ForumComment.objects.all()[::-1]
    print("posts",posts)
    args = {
        'posts': posts,
        'comments':comments,
    }
    return render(request , 'forum/forums.html' , args)

def create_post(request):
    if not request.user.is_authenticated():
        return render(request, 'accounts/login.html')
    else:
        form = ForumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.user = request.user
            forum.save()
            return redirect('forum:forums')
        context = {
            "form": form,
        }
        return render(request, 'forum/create_post.html', context)


def post_comment(request, post_id):
    if not request.user.is_authenticated():
        return redirect('accounts:login')
    else:
        get_post = Forum.objects.get(id=post_id)
        if request.method == 'POST' :
            form = ForumCommentForm(request.POST or None)
            if form.is_valid() :
                mycomment = form.save(commit=False)
                comment = form.cleaned_data['comment']
                mycomment.forum = get_post
                mycomment.user = request.user
                mycomment.save()
                print("\nform is valid!!!!\n")
                return redirect('forum:forums')
            else:
                print("\nform is not valid!!\n")
                return redirect('forum:forums')
        else:
            form = ForumCommentForm(request.POST or None)
            args = { 
            'form':form
             }
            return render(request, 'forum/forums.html', args)

def delete_post(request, post_id):
    post = Forum.objects.get(pk=post_id)
    post.delete()
    posts = Forum.objects.all()[::-1]
    return redirect('forum:forums')

