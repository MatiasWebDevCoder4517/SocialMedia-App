from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Talk


@login_required
def feed(request):
    userids = [request.user.id]

    for talker in request.user.talkerprofile.follows.all():
        userids.append(talker.user.id)

    talks = Talk.objects.filter(created_by_id__in=userids)

    for talk in talks:
        likes = talk.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            talk.liked = True
        else:
            talk.liked = False

    return render(request, 'feed/feed.html', {'talks': talks})


@login_required
def search(request):
    query = request.GET.get('query', '')

    if len(query) > 0:
        talkers = User.objects.filter(username__icontains=query)
        talks = Talk.objects.filter(body__icontains=query)
    else:
        talkers = []
        talks = []

    context = {
        'query': query,
        'talkers': talkers,
        'talks': talks
    }

    return render(request, 'feed/search.html', context)
