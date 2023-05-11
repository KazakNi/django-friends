from djoser.serializers import UserCreateSerializer as BaseDjoserUserSerializer
from users.models import MyUser, FriendshipRequest, Friendship
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers


class BaseUserSerializer(BaseDjoserUserSerializer):

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email')


class RequestSerializer(ModelSerializer):
    outcoming = SerializerMethodField()
    incoming = SerializerMethodField()
    
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'outcoming', 'incoming')

    def get_outcoming(self, obj):
        serializer = BaseUserSerializer(instance=self.context['outcoming'],
                                        many=True)
        return serializer.data

    def get_incoming(self, obj):
        serializer = BaseUserSerializer(instance=self.context['incoming'],
                                        many=True)
        return serializer.data


class FriendSerializer(ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('__all__')


class FriendshipSerializer(ModelSerializer):
    friends = SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'friends')

    def get_friends(self, obj):
        serializer = BaseUserSerializer(instance=self.context['friends'],
                                        many=True)
        return serializer.data
