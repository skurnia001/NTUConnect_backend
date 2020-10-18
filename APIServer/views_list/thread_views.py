from rest_framework import generics

from APIServer.models import Thread, ForumJoined
from APIServer.serializers import ThreadSerializer, ThreadListSerializer, ThreadSpecificSerializer

## Thread API

class ThreadCreation(generics.CreateAPIView):
    """
    Create a new Thread
    """
    serializer_class = ThreadSerializer

class ThreadSpecific(generics.RetrieveAPIView):
    """
    View a specific thread (also provide all messages in that thread) - See specific thread
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSpecificSerializer

class ThreadList(generics.ListAPIView):
    """
    List all thread that current user has joined
    """
    serializer_class = ThreadListSerializer

    def get_queryset(self):
        forums_joined = ForumJoined.objects.filter(user=self.request.user).values('forum')
        forums_id = []
        for data in forums_joined:
            forums_id.append(data["forum"])
        threads = Thread.objects.filter(forum__in=forums_id)
        return threads

# class ThreadList(generics.ListAPIView):
#     """
#     List all Thread
#     """
#     queryset = Thread.objects.all()
#     serializer_class = ThreadListSerializer




