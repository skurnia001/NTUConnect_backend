# users/urls.py
from django.urls import path

from .views import UserList, UserDetail

from APIServer.views_list.forum_views import ForumCreation, ForumList, ForumSpecific
from APIServer.views_list.thread_views import ThreadCreation, ThreadList, ThreadSpecific
from APIServer.views_list.message_views import MessageCreation, MessageIsSolved

urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('forum/', ForumCreation.as_view()),
    path('forums/', ForumList.as_view()),
    path('forum/<int:pk>', ForumSpecific.as_view()),
    path('thread/', ThreadCreation.as_view()),
    path('threads/', ThreadList.as_view()),
    path('thread/<int:pk>/', ThreadSpecific.as_view()),
    path('message/', MessageCreation.as_view()),
    path('message/<int:pk>', MessageIsSolved.as_view()),
]