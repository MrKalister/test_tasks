from django.db import models


class BaseAbstractModel(models.Model):
    """Basic abstract model."""

    name = models.CharField(verbose_name='Название', max_length=128)

    class Meta:
        ordering = ['name']
        abstract = True

    def __str__(self):
        return self.name


class Category(BaseAbstractModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class City(BaseAbstractModel):
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Advert(models.Model):
    title = models.CharField(
        verbose_name='Заголовок', max_length=128, db_index=True
    )
    description = models.TextField(verbose_name='Описание')
    city = models.ForeignKey(
        verbose_name='Город',
        to='api.City',
        on_delete=models.CASCADE,
        related_name='adverts',
    )
    category = models.ForeignKey(
        verbose_name='Категория',
        to='api.Category',
        on_delete=models.CASCADE,
        related_name='adverts',
    )
    views = models.PositiveIntegerField(verbose_name='Просмотры', default=0)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        null=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['id']

    def __str__(self):
        return self.title
