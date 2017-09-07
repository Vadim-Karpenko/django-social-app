from django.contrib import admin
from .models import Image, Comment

class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'created']
    list_filter = ['created']

admin.site.register(Image, ImageAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'created', 'active')
    list_filter = ('created', 'active')
    search_fields = ('user', 'body')

admin.site.register(Comment, CommentAdmin)
