from rest_framework import generics

from APIServer.models import Message
from APIServer.serializers import MessageSerializer, MessageSolvedSerializer

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



