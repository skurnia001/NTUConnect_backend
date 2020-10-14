from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Forum, Thread, Message


class CustomUserAdmin(UserAdmin):
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Forum)
admin.site.register(Thread)
admin.site.register(Message)
