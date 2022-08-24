from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'created_at')
    fields = (('title', 'subtitle', 'slug'), 'author', 'image', 'content', 'deleted')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'subtitle', 'content')
    prepopulated_fields = {'slug': ('title',)}
