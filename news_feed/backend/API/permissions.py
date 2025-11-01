from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrAdminOrLikeOrRead(BasePermission):
    def is_owner(self, request, obj):
        """The author of his post can delete foreign comments."""

        if getattr(obj, 'post_id', None):
            return obj.post.author == request.user

    def has_object_permission(self, request, view, obj):

        return (
            request.method in SAFE_METHODS
            or view.action == 'like'
            or obj.author == request.user
            or request.user.is_staff
            or self.is_owner(request, obj)
        )
