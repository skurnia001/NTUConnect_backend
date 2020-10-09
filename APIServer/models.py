from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import Truncator

from datetime import datetime

class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.email

class Forum(models.Model):
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=100)

    ## todo -> is cascade okay here?
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_code


class Thread(models.Model):
    ## todo -> is cascade okay here?
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='threads')

    title = models.CharField(max_length=100)
    solved = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, blank=True)
    date_posted = models.DateTimeField(default=datetime.now, blank=True)

    # tbd
    # class Meta:
    #     ordering = ('date_posted', )

    def __str__(self):
        return self.title

class Message(models.Model):
    ## todo -> is cascade okay here?
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')

    upvote = models.IntegerField(default=0)
    content = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        ordering = ('date_posted',)

    def __str__(self):
        # truncated_content = Truncator(self.content)
        # return truncated_content.chars(25)
        return self.content