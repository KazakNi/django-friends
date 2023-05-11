from users.models import FriendshipRequest, MyUser, Friendship
from .serializers import RequestSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import models


def get_requests(user):
    query = FriendshipRequest.objects.select_related('from_user')
    from_ = (query.filter(from_user=user).
             annotate(recipients=models.F('to_user__username')).
             values('recipients'))
    to_me = (query.filter(to_user=user).
             annotate(senders=models.F('from_user__username')).
             values('senders'))
    outcoming_requests = [request['recipients'] for request in from_]
    incoming_requests = [request['senders'] for request in to_me]
    outcoming = MyUser.objects.filter(username__in=outcoming_requests)
    incoming = MyUser.objects.filter(username__in=incoming_requests)
    return outcoming, incoming


def check_friendship(user, follower) -> bool:
    return (Friendship.objects.filter((
            models.Q(follower=user, following=follower) |
            models.Q(follower=follower, following=user))).exists())


def get_friends(user):
    friends = []
    query = Friendship.objects.select_related('following')
    my_friends = (query.filter(following=user).annotate(
        friends=models.F('follower__username')).values('friends'))
    for friend in my_friends:
        friends.append(friend['friends'])
    i_am_in_friends = (query.filter(follower=user).
                       annotate(friends=models.F('following__username')).
                       values('friends'))
    for friend in i_am_in_friends:
        friends.append(friend['friends'])
    query = MyUser.objects.filter(username__in=friends)
    return query


def delete_request(user, pk):
    follower = MyUser.objects.get(id=pk)
    obj = get_object_or_404(FriendshipRequest, from_user=follower,
                            to_user=user)
    obj.delete()
