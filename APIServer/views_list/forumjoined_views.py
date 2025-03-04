from rest_framework import generics, permissions

from APIServer.models import ForumJoined as ForumJoinedModel
from APIServer.serializers import (
    ForumJoinedSerializer
)

## Seems not needed anymore
class ForumJoined(generics.ListAPIView):
    """
    List all forum that current user has joined
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ForumJoinedSerializer

    def get_queryset(self):
        forums_joined = ForumJoinedModel.objects.filter(user=self.request.user)
        return forums_joined