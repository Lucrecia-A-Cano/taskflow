from rest_framework import permissions
from .models import SecurityLog
from .services import MembershipService


class IsProjectAdminOrReadOnly(permissions.BasePermission):
    """
    Cualquier miembro del proyecto puede leer.
    Solo un admin del proyecto puede modificar (editar/borrar).
    Sirve tanto para Task (obj.project) como para Project (obj).
    """

    def has_object_permission(self, request, view, obj):
        project = obj.project if hasattr(obj, "project") else obj
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return MembershipService.is_member(request.user, project)

        allowed = MembershipService.is_admin(request.user, project)
        if not allowed:
            SecurityLog.objects.create(
                user=request.user,
                action="permission_denied",
                detail=f"{request.method} {request.path}",
                ip_address=request.META.get("REMOTE_ADDR"),
            )
        return allowed