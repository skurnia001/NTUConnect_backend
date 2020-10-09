from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Forum, Thread, Message
from .serializers import UserSerializer, ForumSerializer, ThreadSerializer, MessageSerializer

CustomUser = get_user_model()


class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


## todo ! should we separate this into different file?

## Forum API

class ForumCreation(generics.CreateAPIView):
    serializer_class = ForumSerializer

class ForumList(generics.ListAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer


## Thread API

class ThreadCreation(generics.CreateAPIView):
    serializer_class = ThreadSerializer

class ThreadList(generics.ListAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    # def get_queryset(self, *args, **kwargs):
    #     threads = Thread.objects.filter(forum__id=self.kwargs.get('pk'))
    #     print(threads.values())
    #     serializer = ThreadSerializer(threads)
    #     return Response(serializer.data)

# class ThreadList(APIView):
#     def get(self, request, format=None):
#         pk = self.kwargs.get('pk')
#         threads = Thread.objects.filter(forum__id=pk)
#         return Response(threads)


## Is this needed ?
class ThreadSpecific(generics.RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


## Message (comment / reply) API

class MessageCreation(generics.CreateAPIView):
    serializer_class = MessageSerializer


