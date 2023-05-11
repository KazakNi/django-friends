from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from users.models import FriendshipRequest, Friendship
from users.models import MyUser
from rest_framework.decorators import action
from .serializers import (BaseUserSerializer, RequestSerializer,
                          FriendshipSerializer)
from django.shortcuts import get_object_or_404
from .utils import get_requests, delete_request, get_friends, check_friendship
from django.db.transaction import atomic
from django.db import models


class FriendShipViewset(ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer

    @action(methods=['delete'], detail=True)
    def delete_friend(self, request, pk=None):
        """Удалить пользователя из друзей."""
        user = self.request.user
        follower = MyUser.objects.get(id=pk)
        obj = get_object_or_404(Friendship, (models.Q(follower=user,
                                                      following=follower)
                                             | models.Q(follower=follower,
                                                        following=user)))
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def get_status(self, request, pk=None):
        """Получить статус отношений с пользователем."""
        user = self.request.user
        target_user = MyUser.objects.get(id=pk)
        friends = check_friendship(user, target_user)
        request_from_me = (FriendshipRequest.objects.
                           filter(from_user=user, to_user=target_user).
                           exists())
        request_from_him = (FriendshipRequest.objects.
                            filter(from_user=target_user, to_user=user).
                            exists())
        serializer = BaseUserSerializer(
                        target_user, many=False)
        headers = self.get_success_headers(serializer.data)
        if friends:
            return Response(
             {"Статус": f"Вы в друзьях у {target_user}."},
             status=status.HTTP_201_CREATED,
             headers=headers)
        elif request_from_me:
            return Response(
             {"Статус": "Вы ожидаете ответа на Вашу заявку"
              f"в друзья {target_user}."},
             status=status.HTTP_201_CREATED,
             headers=headers)
        elif request_from_him:
            return Response(
             {"Статус": f"{target_user} ожидает"
              " ответа на свою заявку в друзья."},
             status=status.HTTP_201_CREATED,
             headers=headers)
        else:
            Response({'message':
                      f'Вы ещё не взаимодействовали с {target_user}'})

    def list(self, request, *args, **kwargs):
        user = self.request.user
        result = get_friends(user)
        data = {'friends': set(result)}
        serializer = FriendshipSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data,
                            status=status.HTTP_200_OK)


class RequestViewSet(ModelViewSet):
    queryset = FriendshipRequest.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RequestSerializer
        return BaseUserSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        from_me, to_me = get_requests(user)
        data = {'outcoming': from_me, 'incoming': to_me}
        serializer = RequestSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data,
                            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def send(self, request, pk=None):
        """Отправить заявку в друзья."""
        user = self.request.user
        following = MyUser.objects.get(id=pk)
        meeting_query = FriendshipRequest.objects.filter(from_user_id=pk,
                                                         to_user=user)
        if user == following:
            return Response({'message': 'Вы не можете отправить заявку сам себе!'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif meeting_query.exists():
            meeting_query.delete()
            return self.accept(request, pk=pk)
        elif check_friendship(user, following):
            return Response({'message': 'Вы уже друзьях!'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            frendship_request, created = (FriendshipRequest.objects.
                                          get_or_create(from_user=user,
                                                        to_user=following))
            if created:
                serializer = BaseUserSerializer(
                        following, many=False)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'Вы уже отправили заявку!'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True)
    def decline(self, request, pk=None):
        """Отклонить заявку в друзья."""
        user = self.request.user
        delete_request(user=user, pk=pk)
        return Response({'message': 'Запрос в друзья отклонён!'})

    @atomic
    @action(methods=['post'], detail=True)
    def accept(self, request, pk=None):
        """Принять заявку в друзья."""
        user = self.request.user
        follower = MyUser.objects.get(id=pk)
        frendship_acception, created = Friendship.objects.get_or_create(
                following=user, follower=follower)
        if created:
            serializer = BaseUserSerializer(
                    follower, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message': 'Вы уже добавлены!'},
                        status=status.HTTP_400_BAD_REQUEST)
