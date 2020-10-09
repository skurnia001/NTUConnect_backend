# users/urls.py
from django.urls import path

from .views import (
    UserList,
    UserDetail,
    ForumCreation,
    ForumSpecific,
    ForumList,
    ThreadCreation,
    ThreadList,
    ThreadSpecific,
    MessageCreation
)

urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('createforums/', ForumCreation.as_view()),
    path('forumlist/', ForumList.as_view()),
    path('forumspec/<int:pk>', ForumSpecific.as_view()),
    path('createthreads/', ThreadCreation.as_view()),
    path('threadlist/', ThreadList.as_view()),
    path('threadspec/<int:pk>/', ThreadSpecific.as_view()),
    path('createmessages/', MessageCreation.as_view()),
]