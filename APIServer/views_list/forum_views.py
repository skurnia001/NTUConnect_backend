from rest_framework import generics

from APIServer.models import Forum
from APIServer.serializers import (
    ForumSerializer,
    ForumListSerializer,
    ForumSpecificSerializer,
    ForumSubscriptionSerializer
)

class ForumCreation(generics.CreateAPIView):
    """
    Create a new Forum (teacher only)
    """
    serializer_class = ForumSerializer

class ForumList(generics.ListAPIView):
    """
    List all Forum
    """
    queryset = Forum.objects.all()
    serializer_class = ForumListSerializer

class ForumSpecific(generics.RetrieveAPIView):
    """
    View a specific forum and provide all threads (See all threads in specific course)
    """
    queryset = Forum.objects.all()
    serializer_class = ForumSpecificSerializer

class ForumSubscription(generics.CreateAPIView):
    """
    Student can join a forum
    """
    serializer_class = ForumSubscriptionSerializer

