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
<<<<<<< HEAD
    Mark a message (reply) as correct - also update the corresponding thread (only 1 message is allow to be correct)
=======
    Mark a message (reply) as correct - also update the corresponding thread
>>>>>>> 3bd48d320a52faa626cfc92734ca46b2efd03043
    """
    queryset = Message.objects.all()
    serializer_class = MessageSolvedSerializer



