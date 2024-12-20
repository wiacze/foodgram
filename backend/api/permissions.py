from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminIsAuthorOrReadOnly(BasePermission):

    message = 'У вас недостаточно прав для данного действия.'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_admin
                or request.user.is_staff
                or request.user == obj.author
            )
        )


class AllowAny(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'me':
            return request.user.is_authenticated
        return True
