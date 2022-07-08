
from django.urls import reverse
from re import template
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from PostFeed.models import Posts,Stream,Tag,Likes
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from PostFeed.form import newPost
from Comment.models import Comment
from Comment.form import CommentForms

# from .forms import PostFormuser




@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)

    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)
    
    post_items = Posts.objects.filter(id__in=group_ids).all().order_by('-posted')

    template = loader.get_template('Feed/index.html')

    context = {
        'post_items': post_items,
    }

    return HttpResponse(template.render(context, request))

@login_required
def PostDetails(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    user = request.user
    comments = Comment.objects.filter(post=post).order_by('date')

    if request.method == "POST":
        form = CommentForms(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('postdetail', args=[post_id]))
        else:
            form = CommentForms()


    template = loader.get_template('Feed/postdetails.html')

    context = {
        'post': post
    }

    
    return HttpResponse(template.render(context, request))

@login_required
def NewPost(request):
    user = request.user.id
    tags_obj = []

    if request.method == "POST":
        form = newPost(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p ,created = Posts.objects.get_or_create(pictures=picture, caption=caption, user_id = user)
            p.tags.set(tags_obj)
            p.save()

            return redirect('feeds')
    else:
        form = newPost()

    context = {
        "form": form
        }
    return render(request,'Feed/newpost.html', context)

@login_required
def tags(request, tag_slug):
    tag = get_object_or_404(Tag,slug=tag_slug)
    posts = Posts.objects.filter(tags=tag).order_by('-posted')

    template = loader.get_template('Feed/tags.html')

    context = {
        'posts': posts,
        'tag': tag
    }

    return HttpResponse(template.render(context, request))

@login_required
def like(request, post_id):
    user = request.user
    post = Posts.objects.get(id=post_id)
    current_likes = post.like

    liked = Likes.objects.filter(user=user, posts=post).count()

    if not liked:
        like = Likes.objects.create(user=user,posts=post)
        current_likes = current_likes + 1

    else:
        Likes.objects.filter(user=user, posts=post).delete()

        current_likes = current_likes - 1

    post.like = current_likes
    post.save()

    return HttpResponseRedirect(reverse('postdetail', args=[post_id]))

    



    




    


