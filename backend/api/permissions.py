from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminIsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_admin
                or request.user == obj.author
            )
        )
