from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'courses')



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile,UserProfileAdmin)