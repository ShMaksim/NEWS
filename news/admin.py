from django.contrib import admin
from .models import Post, Category, Comment
from modeltranslation.admin import TranslationAdmin


class PostAdmin(TranslationAdmin):
    list_display = ('title', 'author', 'post_type', 'created_at', 'rating')
    list_filter = ('post_type', 'created_at', 'categories')
    search_fields = ('title', 'text')
    search_date = 'created_ad'

class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at', 'rating')
    list_filter = ('created_at', 'rating')
    search_fields = ('post_title', 'user_username', 'text')
    search_date = 'created_at'


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
