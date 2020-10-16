from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from APIServer.models import Forum, Thread, Message, ForumJoined


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'score']


class ForumSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Forum
        fields = ['id', 'course_code', 'course_title', 'creator']

class ForumSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ForumJoined
        fields = ['forum', 'user']

    # def update(self, instance, validated_data):
    #     ForumJoined.objects.create(user=validated_data.get('user'), forum=instance)
    #     return instance

class ForumListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forum
        fields = ['id', 'course_code', 'course_title', 'creator']

class ThreadSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Thread
        fields = ['id', 'title', 'solved', 'description', 'date_posted', 'creator', 'forum']

class ThreadListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = ['id', 'title', 'solved', 'description', 'date_posted', 'creator', 'forum']

class ForumSpecificSerializer(serializers.ModelSerializer):
    threads = ThreadListSerializer(many = True)

    class Meta:
        model = Forum
        fields = ['id', 'course_code', 'course_title', 'creator', 'threads']

class MessageSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

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
        if instance.thread.solved == False and message_status_update == True:
            instance.is_correct = message_status_update
            instance.thread.solved = message_status_update

            ## Temporary Counter
            instance.creator.score += 5

            instance.save()
            instance.thread.save()
            instance.creator.save()
        return instance

class MessageVoteSerializer(serializers.ModelSerializer):
    is_upvote = serializers.BooleanField(write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'thread', 'upvote', 'is_correct', 'date_posted', 'creator', 'date_posted', 'is_upvote']

    def update(self, instance, validated_data):
        is_upvote = validated_data.get('is_upvote', None)
        if is_upvote is None:
            return instance

        if is_upvote:
            instance.upvote += 1
            instance.creator.score += 1
        else:
            instance.upvote -= 1
            instance.creator.score -= 1

        instance.save()
        instance.creator.save()
        return instance