from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Category, City, Advert


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = list_filter = search_fields = ('id', 'name')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = list_filter = search_fields = ('id', 'name')


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = search_fields = (
        'id',
        'title',
        'description',
        'city',
        'category',
        'views',
        'pub_date',
    )
    list_filter = ('city', 'category', 'views', 'pub_date')
    readonly_fields = ('views',)


AdminSite.empty_value_display = '-empty-'
