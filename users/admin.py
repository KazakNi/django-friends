from django.contrib import admin
from .models import Friendship, FriendshipRequest, MyUser


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id')


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    pass


@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    pass
