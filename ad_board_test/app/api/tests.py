from api.models import Advert, City, Category
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AdvertViewTestCase(APITestCase):
    def setUp(self):
        self.city = City.objects.create(name='Kazan')
        self.category = Category.objects.create(name='First')
        self.advert = Advert.objects.create(
            title='Test Advert',
            description='Test Advert',
            city=self.city,
            category=self.category,
        )

    def test_retrieve_advert(self):
        url = reverse('advert-detail', kwargs={'pk': self.advert.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_up_views(self):
        initial_views = self.advert.views
        url = reverse('advert-detail', kwargs={'pk': self.advert.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.advert.refresh_from_db()
        self.assertEqual(self.advert.views, initial_views + 1)

    def test_list_adverts(self):
        url = reverse('advert-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
