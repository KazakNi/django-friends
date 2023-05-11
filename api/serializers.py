from djoser.serializers import UserCreateSerializer as BaseDjoserUserSerializer
from users.models import MyUser, FriendshipRequest, Friendship
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ListField
from rest_framework import serializers


class BaseUserSerializer(BaseDjoserUserSerializer):

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email')


class RequestSerializer(serializers.Serializer):
    outcoming = ListField()
    incoming = ListField()


class FriendSerializer(ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('__all__')


class FriendshipSerializer(ModelSerializer):
    friends = ListField()

    class Meta:
        model = MyUser
        fields = ('friends',)
