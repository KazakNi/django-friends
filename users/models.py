from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=150, blank=False,
                              null=False)
    username = models.CharField(unique=True, max_length=150, blank=False,
                                null=False)
    password = models.CharField(max_length=150, blank=False, null=False)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Friendship(models.Model):
    following = models.ForeignKey(MyUser, related_name='following',
                                  on_delete=models.CASCADE)
    follower = models.ForeignKey(MyUser, related_name='follower',
                                 on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('following', 'follower'),
                name='unique friendship')]
        verbose_name = 'В друзьях'
        verbose_name_plural = 'Друзья'

    def __str__(self):
        return f'{self.follower} в друзьях у {self.following}'


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(MyUser, related_name='from_user',
                                  on_delete=models.CASCADE)
    to_user = models.ForeignKey(MyUser, related_name='to_user',
                                on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('from_user', 'to_user'),
                name='unique request')]
        verbose_name = 'Заявка в друзья'
        verbose_name_plural = 'Заявки в друзья'

    def __str__(self):
        return f'{self.from_user} отправил заявку в друзья {self.to_user}'
