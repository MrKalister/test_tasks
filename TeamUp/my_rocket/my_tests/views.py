from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets

from .models import EQTestResult, IQTestResult, UniqueLogin
from .serializers import (CreateTestSerializer, EQTestResultSerializer,
                          GetTestSerializer, IQTestResultSerializer)


class ResultCreateView(generics.CreateAPIView):
    def get_login(self, login):
        return get_object_or_404(UniqueLogin, unique_string=login)

    def create(self, request, *args, **kwargs):
        request.data['login'] = self.get_login(request.data['login']).pk
        return super().create(request, *args, **kwargs)


class EQTestResultCreateView(ResultCreateView):
    queryset = EQTestResult.objects.all()
    serializer_class = EQTestResultSerializer


class IQTestResultCreateView(ResultCreateView):
    queryset = IQTestResult.objects.all()
    serializer_class = IQTestResultSerializer


class TestView(mixins.ListModelMixin, mixins.CreateModelMixin,
               mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = UniqueLogin.objects.all()
    lookup_field = 'unique_string'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTestSerializer
        return GetTestSerializer
