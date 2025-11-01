from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models import F

from .models import Advert
from .serializers import AdvertSerializer


class AdvertListView(ListAPIView):
    """
    Provides information about Adverts.
    """

    queryset = Advert.objects.select_related('city', 'category')
    serializer_class = AdvertSerializer


class AdvertDetailView(RetrieveAPIView):
    """
    Provides information about Advert.
    """

    queryset = Advert.objects.select_related('city', 'category')
    serializer_class = AdvertSerializer

    def get_object(self):
        instance = super().get_object()
        self.up_views(instance)
        instance.refresh_from_db()
        return instance

    def up_views(self, instance: Advert) -> None:
        # Это способ может предотвратить проблемы,
        # возникающие при параллельных изменениях.
        Advert.objects.filter(pk=instance.pk).update(views=F('views') + 1)
