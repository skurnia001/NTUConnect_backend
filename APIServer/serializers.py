from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
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
        fields = ['id', 'content', 'thread', 'upvote', 'is_correct', 'date_posted', 'creator', 'date_posted', 'reply']

class MessageReplySerializer(serializers.ModelSerializer):
    replies = RecursiveField(many=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'thread', 'upvote', 'is_correct', 'date_posted', 'creator', 'date_posted', 'replies']

class ThreadSpecificSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField('get_parent_messages')

    class Meta:
        model = Thread
        fields = ['id', 'title', 'solved', 'description', 'date_posted', 'creator', 'forum', 'messages']

    def get_parent_messages(self, thread):
        parent_messages = Message.objects.filter(thread=thread, reply__isnull=True)
        serializer = MessageReplySerializer(instance=parent_messages, many=True)
        return serializer.data


class MessageSolvedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'content', 'thread', 'upvote', 'is_correct', 'date_posted', 'creator', 'date_posted']

    def update(self, instance, validated_data):
        message_status_update = validated_data.get('is_correct', instance.is_correct)
        if instance.thread.solved == False:
            instance.is_correct = message_status_update
            instance.thread.solved = message_status_update
            instance.save()
            instance.thread.save()
        return instance
