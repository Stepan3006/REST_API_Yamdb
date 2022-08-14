from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin to access.
    """

    def has_permission(self, request, view):
        return request.user.is_admin


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow admin or owner to access.
    """

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and (
                request.user.is_admin
            )
        )


class IsReviewPerm(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.role == 'moderator'
        )


class IsAuthorModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (obj.author == request.user
                and request.user.is_authenticated)
            or request.user.role == 'moderator'
            or request.user.is_admin
        )
