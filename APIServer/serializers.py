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
        fields = ['id', 'course_code', 'course_title', 'creator']

class ThreadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = ['id', 'title', 'solved', 'description', 'date_posted', 'creator', 'forum']

class ForumSpecificSerializer(serializers.ModelSerializer):
    threads = ThreadSerializer(many = True)

    class Meta:
        model = Forum
        fields = ['id', 'course_code', 'course_title', 'creator', 'threads']

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'content', 'thread', 'upvote', 'is_correct', 'date_posted', 'creator', 'date_posted']


class ThreadSpecificSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many = True)

    class Meta:
        model = Thread
        fields = ['id', 'title', 'solved', 'description', 'date_posted', 'creator', 'forum', 'messages']


class MessageSolvedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'content', 'thread', 'upvote', 'is_correct', 'date_posted', 'creator', 'date_posted']

    def update(self, instance, validated_data):
        message_status_update = validated_data.get('is_correct', instance.is_correct)
        instance.is_correct = message_status_update
        instance.thread.solved = message_status_update
        instance.save()
        instance.thread.save()
        return instance
