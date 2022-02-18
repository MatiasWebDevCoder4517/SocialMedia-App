from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TalkerProfileForm, UserRegisterForm, UserUpdateForm, TalkerProfileUpdateForm
from .models import TalkerProfile, FriendRequest
from apps.feed.models import Talk
from django.conf import settings
from django.http import HttpResponseRedirect
from apps.notification.utilities import create_notification
import random


User = get_user_model()

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


'''
TESTING

### This view will form the user list to be recommended to any user to help them discover new users to make friends with. ###

@login_required
def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    my_friends = request.user.profile.friends.all()
    sent_to = []
    friends = []
    for user in my_friends:
        friend = user.friends.all()
        for f in friend:
            if f in friends:
                friend = friend.exclude(user=f.user)
        friends += friend
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    if request.user.profile in friends:
        friends.remove(request.user.profile)
    random_list = random.sample(list(users), min(len(list(users)), 10))
    for r in random_list:
        if r in friends:
            random_list.remove(r)
    friends += random_list
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    for se in sent_friend_requests:
        sent_to.append(se.to_user)
    context = {
        'users': friends,
        'sent': sent_to
    }
    return render(request, "users/users_list.html", context)
    

'''


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
