from users.models import FriendshipRequest, MyUser
from .serializers import RequestSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


def get_requests(user, actor):
    if actor == 'from_user':
        objects = FriendshipRequest.objects.filter(from_user=user)
        serializer = RequestSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        objects = FriendshipRequest.objects.filter(to_user=user)
        serializer = RequestSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def delete_request(user, pk):
    follower = MyUser.objects.get(id=pk)
    obj = get_object_or_404(FriendshipRequest, from_user=follower,
                            to_user=user)
    obj.delete()
