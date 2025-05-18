from django.contrib import admin
from .models import Post,Comment



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','content','created_at')
    search_fields = ('title',)
    list_filter = ('title',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author','content','created_at')
    search_fields = ('post',)
    list_filter = ('post',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
