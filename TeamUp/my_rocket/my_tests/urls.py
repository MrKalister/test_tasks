from django.urls import include, path
from rest_framework import routers

from .views import EQTestResultCreateView, IQTestResultCreateView, TestView

v1_router = routers.DefaultRouter()
v1_router.register('tests', TestView, basename='test')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('eq-test-results/', EQTestResultCreateView.as_view(),
         name='eq-test-results'),
    path('iq-test-results/', IQTestResultCreateView.as_view(),
         name='iq-test-results'),
]
