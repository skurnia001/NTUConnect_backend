from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from APIServer.models import Thread, ForumJoined
from APIServer.serializers import ThreadSerializer, ThreadListSerializer, ThreadSpecificSerializer

## Thread API

class ThreadCreation(generics.CreateAPIView):
    """
    Create a new Thread
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ThreadSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ThreadSpecific(generics.RetrieveAPIView):
    """
    View a specific thread (also provide all messages in that thread) - See specific thread
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Thread.objects.all()
    serializer_class = ThreadSpecificSerializer

class ThreadList(generics.ListAPIView):
    """
    List all thread that current user has joined
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ThreadListSerializer

    def get_queryset(self):
        forums_joined = ForumJoined.objects.filter(user=self.request.user).values('forum')
        forums_id = []
        for data in forums_joined:
            forums_id.append(data["forum"])
        threads = Thread.objects.filter(forum__in=forums_id)
        return threads

class ThreadSearch(generics.ListAPIView):
    """
    Search a thread
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering = ['-date_posted']




