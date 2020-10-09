from django.contrib.auth import get_user_model
from rest_framework import serializers
from APIServer.models import Forum, Thread, Message


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username',)


class ForumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forum
        fields = ['course_code', 'course_title', 'creator',]

class ThreadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = ['title', 'solved', 'description', 'date_posted', 'creator', 'forum',]


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['content', 'thread', 'upvote', 'is_correct', 'date_posted', 'creator', 'date_posted',]
