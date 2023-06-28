from django.contrib import admin
from .models import Article, Comment


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0  # tells django to not add the default 3 extra inlines


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine,
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
