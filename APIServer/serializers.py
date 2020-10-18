from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from APIServer.models import Forum, Thread, Message, ForumJoined, VoteMessage


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
    is_joined = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Forum
        fields = ['id', 'course_code', 'course_title', 'creator', 'is_joined']

    def get_is_joined(self, forum):
        user = self.context['request'].user
        forum_joined = ForumJoined.objects.filter(user=user, forum=forum).exists()
        return forum_joined



class ThreadListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = ['id', 'title', 'solved', 'description', 'date_posted', 'creator', 'forum']


class ForumSpecificSerializer(serializers.ModelSerializer):
    threads = ThreadListSerializer(many = True)
    is_joined = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Forum
        fields = ['id', 'course_code', 'course_title', 'creator', 'threads', 'is_joined']

    def get_is_joined(self, forum):
        user = self.context['request'].user
        forum_joined = ForumJoined.objects.filter(user=user, forum=forum).exists()
        return forum_joined


class ThreadSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Thread
        fields = ['id', 'title', 'solved', 'description', 'date_posted', 'creator', 'forum']


class ThreadSpecificSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField('get_parent_messages')

    class Meta:
        model = Thread
        fields = ['id', 'title', 'solved', 'description', 'date_posted', 'creator', 'forum', 'messages']

    def get_parent_messages(self, thread):
        parent_messages = Message.objects.filter(thread=thread, reply__isnull=True)
        serializer = MessageReplySerializer(instance=parent_messages, many=True, context=self.context)
        return serializer.data

class MessageSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ['id', 'content', 'thread', 'upvote', 'is_correct', 'date_posted', 'creator', 'date_posted', 'reply']


class MessageReplySerializer(serializers.ModelSerializer):
    replies = RecursiveField(many=True)
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'thread', 'upvote', 'is_correct', 'date_posted', 'creator', 'date_posted', 'replies', 'status']

    def get_status(self, message):
        user = self.context['request'].user
        vote_status = VoteMessage.objects.filter(user=user, message=message)
        if not vote_status:
            ## tbd -> object created can't be serialized directly (?)
            VoteMessage.objects.create(user=user, message=message)
            vote_status = VoteMessage.objects.filter(user=user, message=message)
            serializer = VoteSerialzier(instance=vote_status, many=True)
            return serializer.data
        else:
            serializer = VoteSerialzier(instance=vote_status, many=True)
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
    action = serializers.IntegerField(write_only=True, allow_null=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'thread', 'upvote', 'is_correct', 'date_posted', 'creator', 'date_posted', 'action']

    def update(self, instance, validated_data):
        action = validated_data.get('action', 0)
        if action == 0:
            return instance

        user = self.context['request'].user
        vote_status = VoteMessage.objects.filter(user=user, message=instance)

        if not vote_status:
            vote_status = VoteMessage.objects.create(user=user, message=instance)
        else:
            vote_status = vote_status[0]

        if action == 1:
            if vote_status.value < 1:
                instance.upvote += 1
                instance.creator.score += 1
                vote_status.value = min(1, vote_status.value + 1)
        else:
            if vote_status.value > -1:
                instance.upvote -= 1
                instance.creator.score -= 1
                vote_status.value = max(-1, vote_status.value - 1)

        instance.save()
        instance.creator.save()
        vote_status.save()

        return instance


class VoteSerialzier(serializers.ModelSerializer):

    class Meta:
        model = VoteMessage
        fields = ['value']


class ForumJoinedSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForumJoined
        fields = ['forum']