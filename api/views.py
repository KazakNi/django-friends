from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from users.models import FriendshipRequest, Friendship
from users.models import MyUser
from rest_framework.decorators import action
from .serializers import (BaseUserSerializer, RequestSerializer,
                          FriendshipSerializer)
from django.shortcuts import get_object_or_404
from .utils import get_requests, delete_request
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
        obj = get_object_or_404(Friendship, following=user, follower=follower)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def get_status(self, request, pk=None):
        """Получить статус отношений с пользователем."""
        user = self.request.user
        target_user = MyUser.objects.get(id=pk)
        friends = Friendship.objects.filter((models.Q(follower=user,
                                                      following=target_user)
                                             | models.Q(follower=target_user,
                                                        following=user)))
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
        friends = Friendship.objects.filter(following=user)
        serializer = FriendshipSerializer(
                        friends, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class RequestViewSet(ModelViewSet):
    queryset = FriendshipRequest.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RequestSerializer
        return BaseUserSerializer

    def get_serializer_context(self):
        user = self.request.user
        context = super().get_serializer_context()
        context.update({'user': user})
        return context

    @action(methods=['get'], detail=False)
    def get_incoming_requests(self, request):
        """Посмотреть входящие заявки в друзья."""
        user = self.request.user
        return get_requests(user=user, actor='to_user')

    @action(methods=['get'], detail=False)
    def get_outcoming_requests(self, request):
        """Посмотреть исходящие заявки в друзья."""
        user = self.request.user
        return get_requests(user=user, actor='from_user')

    @action(methods=['post'], detail=True)
    def send(self, request, pk=None):
        """Отправить заявку в друзья."""
        user = self.request.user
        following = MyUser.objects.get(id=pk)
        meeting_query = FriendshipRequest.objects.get(from_user_id=pk,
                                                      to_user=user)
        if meeting_query:
            return self.accept(request, pk=pk)
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
        return Response({'message': 'Запрос в друзья отклонена!'})

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
            delete_request(user=user, pk=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message': 'Вы уже добавлены!'},
                        status=status.HTTP_400_BAD_REQUEST)
