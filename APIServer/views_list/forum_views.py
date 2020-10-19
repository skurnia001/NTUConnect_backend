from rest_framework import generics, permissions

from APIServer.models import Forum
from APIServer.serializers import (
    ForumSerializer,
    ForumListSerializer,
    ForumSpecificSerializer,
    ForumSubscriptionSerializer,
    ForumJoinedSerializer
)
from APIServer.permissions import (
    IsStudent,
    IsInstructor
)

class ForumCreation(generics.CreateAPIView):
    """
    Create a new Forum (teacher only)
    """
    permission_classes = [permissions.IsAuthenticated, IsInstructor]
    serializer_class = ForumSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ForumList(generics.ListAPIView):
    """
    List all Forum
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Forum.objects.all()
    serializer_class = ForumListSerializer

class ForumSpecific(generics.RetrieveAPIView):
    """
    View a specific forum and provide all threads (See all threads in specific course)
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Forum.objects.all()
    serializer_class = ForumSpecificSerializer

class ForumSubscription(generics.CreateAPIView):
    """
    Student can join a forum
    """
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = ForumSubscriptionSerializer


# class ForumSubscriptionV2(generics.UpdateAPIView):
#     """
#     Student can join a forum - f
#     """
#     queryset = Forum.objects.all()
#     serializer_class = ForumSubscriptionSerializer

