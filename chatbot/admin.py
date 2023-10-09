from django.contrib import admin

# Register your models here.

from .models import User, Chat, ChatSession

admin.site.register(User)
admin.site.register(Chat)
admin.site.register(ChatSession)
