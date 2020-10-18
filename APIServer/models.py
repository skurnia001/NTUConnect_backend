from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from datetime import datetime


class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.email


class Forum(models.Model):
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=100)

    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_code

## Tbd - move to signals.py
## find how to trigeer the signals on different file

def create_forum_joined(sender, instance, **kwargs):
    if kwargs['created']:
        ForumJoined.objects.create(user=instance.creator, forum=instance)

post_save.connect(create_forum_joined, sender=Forum)


class Thread(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='threads')

    title = models.CharField(max_length=100)
    solved = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, blank=True)
    date_posted = models.DateTimeField(default=datetime.now, blank=True)

    # class Meta:
    #     ordering = ('date_posted', )

    def __str__(self):
        return self.title


class Message(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')

    upvote = models.IntegerField(default=0)
    content = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=datetime.now, blank=True)
    reply = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        ordering = ('date_posted',)

    def __str__(self):
        return self.content

class ForumJoined(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class VoteMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    value = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + " status: " + str(self.value)
