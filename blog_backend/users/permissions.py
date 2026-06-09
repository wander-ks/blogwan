from rest_framework import permissions
# 该权限可在其他模块（如文章、评论）中使用，用户模块本身暂不需要。
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级权限：只有拥有者可以修改/删除，其他人仅可读
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # 假设 obj 具有 author 或 user 属性，此处通用
        return obj.author == request.user or obj.user == request.user


