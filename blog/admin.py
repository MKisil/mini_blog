from django.contrib import admin

from blog.models import *


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1
    readonly_fields = ('user',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'draft', 'slug')
    list_display_links = ('id', 'title')
    list_editable = ('draft',)
    search_fields = ('id', 'title')
    inlines = [CommentInline]
    save_on_top = True
    save_as = True


@admin.register(Author)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'article')
    list_display_links = ('id',)
    search_fields = ('id', 'user', 'article')
    readonly_fields = ('article', 'user')

