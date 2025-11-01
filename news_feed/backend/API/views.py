from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from posts.models import Post
from .permissions import IsOwnerOrAdminOrLikeOrRead
from .serializers import (CommentSerializer, CreatePostSerializer,
                          GetPostSerializer)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().select_related(
        'author').prefetch_related('likes', 'comments')
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrLikeOrRead)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetPostSerializer
        return CreatePostSerializer

    @action(methods=['post', 'delete'], detail=True)
    def like(self, request, pk):
        """Add and delete like for a post."""

        post = self.get_object()
        if request.method == 'POST':
            post.likes.add(request.user)
            return Response(status=status.HTTP_201_CREATED)
        post.likes.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrLikeOrRead)
    # exclude requests like 'put'
    http_method_names = ['get', 'post', 'delete']

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all().select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
