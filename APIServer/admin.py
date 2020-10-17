from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Forum, Thread, Message, ForumJoined, VoteMessage


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('score',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Forum)
admin.site.register(Thread)
admin.site.register(Message)
admin.site.register(ForumJoined)
admin.site.register(VoteMessage)