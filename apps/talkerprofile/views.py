from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import TalkerProfileForm
from apps.notification.utilities import create_notification


def talkerprofile(request, username):
    user = get_object_or_404(User, username=username)
    talks = user.talks.all()

    for talk in talks:
        likes = talk.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            talk.liked = True
        else:
            talk.liked = False

    context = {
        'user': user,
        'talks': talks
    }

    return render(request, 'talkerprofile/talkerprofile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = TalkerProfileForm(request.POST, request.FILES,
                                 instance=request.user.talkerprofile)

        if form.is_valid():
            form.save()

            return redirect('talkerprofile', username=request.user.username)
    else:
        form = TalkerProfileForm(instance=request.user.talkerprofile)

    context = {
        'user': request.user,
        'form': form
    }

    return render(request, 'talkerprofile/edit_profile.html', context)


@login_required
def follow_talker(request, username):
    user = get_object_or_404(User, username=username)

    request.user.talkerprofile.follows.add(user.talkerprofile)

    create_notification(request, user, 'follower')

    return redirect('talkerprofile', username=username)


@login_required
def unfollow_talker(request, username):
    user = get_object_or_404(User, username=username)

    request.user.talkerprofile.follows.remove(user.talkerprofile)

    return redirect('talkerprofile', username=username)


def followers(request, username):
    user = get_object_or_404(User, username=username)

    """ context = {
        {'user': user}
    } """

    return render(request, 'talkerprofile/followers.html', {'user': user})


def follows(request, username):
    user = get_object_or_404(User, username=username)

    """ context = {
        {'user': user}
    } """

    return render(request, 'talkerprofile/follows.html', {'user': user})
