from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core import serializers as jsonserializer
from APIServer.models import Forum, Thread, Message


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username',)


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['course_code', 'course_title', 'creator']

class ForumSpecificSerializer(serializers.ModelSerializer):
    threads = serializers.SerializerMethodField('get_all_threads')
    class Meta:
        model = Forum
        fields = ['course_code', 'course_title', 'creator', 'threads']

    def get_all_threads(self, forum):
        threads = Thread.objects.filter(forum=forum).values('title', 'description', 'solved', 'date_posted', 'forum', 'creator')
        threads = list(threads)
        return threads

class ThreadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = ['title', 'solved', 'description', 'date_posted', 'creator', 'forum']

class ThreadSpecificSerializer(serializers.ModelSerializer):
    full_messages = serializers.SerializerMethodField('get_full_messages')

    class Meta:
        model = Thread
        fields = ['title', 'solved', 'description', 'date_posted', 'creator', 'forum', 'full_messages']

    def get_full_messages(self, thread):
        messages = Message.objects.filter(thread=thread).values('content', 'creator', 'thread', 'upvote', 'is_correct', 'date_posted')
        messages = list(messages)
        return messages


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['content', 'thread', 'upvote', 'is_correct', 'date_posted', 'creator', 'date_posted']
