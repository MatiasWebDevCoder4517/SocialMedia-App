from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Post


@login_required
def feed(request):
    userids = [request.user.id]

    for poster in request.user.userprofile.follows.all():
        userids.append(poster.user.id)

    posts = Post.objects.filter(created_by_id__in=userids)

    for post in posts:
        likes = post.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            post.liked = True
        else:
            post.liked = False

    context = {
        {'posts': posts}
    }

    return render(request, 'feed/feed.html', context)


@login_required
def search(request):
    query = request.GET.get('query', '')

    if len(query) > 0:
        posters = User.objects.filter(username__icontains=query)
        posts = Post.objects.filter(body__icontains=query)
    else:
        posters = []
        posts = []

    context = {
        'query': query,
        'posters': posters,
        'posts': posts
    }

    return render(request, 'feed/search.html', context)
