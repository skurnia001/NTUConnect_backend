from django.contrib.auth import get_user_model
from rest_framework import generics

from .models import Forum, Thread, Message
from .serializers import UserSerializer, ForumSerializer, ForumSpecificSerializer, ThreadSerializer, ThreadSpecificSerializer, MessageSerializer, MessageSolvedSerializer

CustomUser = get_user_model()


class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


## todo ! should we separate this into different file?

## Forum API

class ForumCreation(generics.CreateAPIView):
    """
    Create a new Forum
    """
    serializer_class = ForumSerializer

class ForumList(generics.ListAPIView):
    """
    List all Forum
    """
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

class ForumSpecific(generics.RetrieveAPIView):
    """
    View a specific forum and provide all threads (See all threads in specific course)
    """
    queryset = Forum.objects.all()
    serializer_class = ForumSpecificSerializer

## Thread API

class ThreadCreation(generics.CreateAPIView):
    """
    Create a new Thread
    """
    serializer_class = ThreadSerializer

class ThreadList(generics.ListAPIView):
    """
    List all Thread - seems not needed ? can be removed later
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

class ThreadSpecific(generics.RetrieveAPIView):
    """
    View a specific thread (also provide all messages in that thread) - See specific thread
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSpecificSerializer


## Message (comment / reply) API

class MessageCreation(generics.CreateAPIView):
    """
    Create a message reply in a thread (ordered by Date Posted)
    """
    serializer_class = MessageSerializer

class MessageIsSolved(generics.RetrieveUpdateAPIView):
    """
    Mark a message (reply) as correct - also update the corresponding thread
    """
    queryset = Message.objects.all()
    serializer_class = MessageSolvedSerializer



