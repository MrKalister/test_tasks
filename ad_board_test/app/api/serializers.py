from rest_framework import serializers

from .models import Advert


class AdvertSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(read_only=True, slug_field='name')
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Advert
        fields = (
            'id',
            'title',
            'description',
            'city',
            'category',
            'views',
            'pub_date',
        )
