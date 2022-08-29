from django.contrib import admin

from .models import Author, Category, Post, PostCategory, Comment, Subscriber


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'rating')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'category', 'time', 'name', 'text', 'rating')
    list_filter = ('author', 'category', 'time')
    search_fields = ('name', 'text')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'text', 'time', 'rating')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscriber)
