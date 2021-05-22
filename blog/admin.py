from django.contrib import admin
from .models import Post,Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'content', 'date_posted')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active') 
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


