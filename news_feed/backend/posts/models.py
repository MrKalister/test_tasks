from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
LIMIT_WORDS = 3


class BaseModel(models.Model):
    """Basic abstract model."""

    text = models.TextField('Текст')
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    header = models.CharField('Заголовок', max_length=50)
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    likes = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='Отметка нравится',
        related_name='liked_posts',
    )

    class Meta:
        ordering = ('-created_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

    def __str__(self):
        return ' '.join(self.header.split()[:LIMIT_WORDS]) + ' ...'


class Comment(BaseModel):
    post = models.ForeignKey(
        Post,
        verbose_name='Новость',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments',
    )

    class Meta:
        ordering = ('-created_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return ' '.join(self.text.split()[:LIMIT_WORDS]) + ' ...'
