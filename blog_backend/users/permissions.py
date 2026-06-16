from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级权限：只有拥有者可以修改/删除，其他人仅可读
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


