# users/urls.py
from django.urls import path

from .views import UserList, UserDetail

from APIServer.views_list.forum_views import ForumCreation, ForumList, ForumSpecific, ForumSubscription
from APIServer.views_list.thread_views import ThreadCreation, ThreadList, ThreadSpecific
from APIServer.views_list.message_views import MessageCreation, MessageIsSolved

urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('forums/create/', ForumCreation.as_view()),
    path('forums/list/', ForumList.as_view()),
    path('forums/<int:pk>/detail/', ForumSpecific.as_view()),
    path('forums/join/', ForumSubscription.as_view()),
    path('threads/create/', ThreadCreation.as_view()),
    path('threads/list/', ThreadList.as_view()),
    path('threads/<int:pk>/detail/', ThreadSpecific.as_view()),
    path('messages/create/', MessageCreation.as_view()),
    path('messages/<int:pk>/mark-solved/', MessageIsSolved.as_view()),
]