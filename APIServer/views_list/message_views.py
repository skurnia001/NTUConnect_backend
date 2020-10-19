from rest_framework import generics, permissions

from APIServer.models import Message
from APIServer.serializers import MessageSerializer, MessageSolvedSerializer, MessageVoteSerializer
from APIServer.permissions import (
    IsStudent,
    IsInstructor
)

## Message (comment / reply) API

class MessageCreation(generics.CreateAPIView):
    """
    Create a message reply in a thread (ordered by Date Posted)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class MessageIsSolved(generics.RetrieveUpdateAPIView):
    """
    Mark a message (reply) as correct - also update the corresponding thread (only 1 message is allow to be correct)
    """
    permission_classes = [permissions.IsAuthenticated, IsInstructor]
    queryset = Message.objects.all()
    serializer_class = MessageSolvedSerializer

class MessageVote(generics.RetrieveUpdateAPIView):
    """
    Upvote or downvote a message (comment)
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageVoteSerializer