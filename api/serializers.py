from djoser.serializers import UserCreateSerializer as BaseDjoserUserSerializer
from users.models import MyUser, FriendshipRequest, Friendship
from rest_framework.serializers import ModelSerializer, ReadOnlyField, PrimaryKeyRelatedField



class BaseUserSerializer(BaseDjoserUserSerializer):

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email')


class RequestSerializer(ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = ('__all__')


class FriendSerializer(ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('__all__')


class FriendshipSerializer(ModelSerializer):
    following = BaseUserSerializer()
    follower_name = ReadOnlyField(source='follower.username')

    class Meta:
        model = Friendship
        fields = ('following', 'follower_name',)
