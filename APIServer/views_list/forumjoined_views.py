from rest_framework import generics

from APIServer.models import ForumJoined as ForumJoinedModel
from APIServer.serializers import (
    ForumJoinedSerializer
)

class ForumJoined(generics.ListAPIView):
    """
    List all forum that current user has joined
    """
    serializer_class = ForumJoinedSerializer

    def get_queryset(self):
        forums_joined = ForumJoinedModel.objects.filter(user=self.request.user)
        return forums_joined