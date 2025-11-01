from django.contrib import admin
from django.db.models import Count
from .models import Post, Comment, LIMIT_WORDS


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _like_count=Count('likes', distinct=True),
            _comments_count=Count('comments', distinct=True),
        )
        return queryset

    list_display = (
        'id',
        'format_header',
        'format_text',
        'author',
        'created_date',
        'extra_field_total_likes',
        'extra_field_total_comments',
    )
    list_filter = search_fields = ('id', 'header', 'author', 'text')

    def format_header(self, obj):
        return str(obj)

    def format_text(self, obj):
        return ' '.join(obj.text.split()[:LIMIT_WORDS]) + ' ...'

    def extra_field_total_likes(self, obj):
        return obj.total_likes()

    def extra_field_total_comments(self, obj):
        return obj.total_comments()

    extra_field_total_likes.short_description = 'Количесвто лайков'
    extra_field_total_comments.short_description = 'Количество комментариев'
    extra_field_total_likes.admin_order_field = '_like_count'
    extra_field_total_comments.admin_order_field = '_comments_count'
    format_text.short_description = 'Текст'
    format_header.short_description = 'Заголовок'
    format_text.admin_order_field = 'text'
    format_header.admin_order_field = 'header'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'post',
        'author',
        'format_text',
        'created_date',
    )
    list_filter = search_fields = (
        'id',
        'post',
        'author',
        'text',
        'created_date',
    )

    def format_text(self, obj):
        return str(obj)

    format_text.short_description = 'Текст'
    format_text.admin_order_field = 'text'


admin.sites.AdminSite.empty_value_display = '-пусто-'
