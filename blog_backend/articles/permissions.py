from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    自定义权限：文章作者才能修改/删除，其他用户只读
    """
    def has_object_permission(self, request, view, obj):
        # 读取方法（GET, HEAD, OPTIONS）允许任何请求
        if request.method in permissions.SAFE_METHODS:
            return True
        # 修改/删除需要作者本人
        return obj.author == request.user