from rest_framework import generics

from APIServer.models import Thread
from APIServer.serializers import ThreadSerializer, ThreadSpecificSerializer

## Thread API

class ThreadCreation(generics.CreateAPIView):
    """
    Create a new Thread
    """
    serializer_class = ThreadSerializer

class ThreadList(generics.ListAPIView):
    """
    List all Thread
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

class ThreadSpecific(generics.RetrieveAPIView):
    """
    View a specific thread (also provide all messages in that thread) - See specific thread
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSpecificSerializer





