from rest_framework import permissions

class IsAuthorOrAdminOrArticleAuthor(permissions.BasePermission):
    """
    自定义权限：
    - 评论作者本人可以修改/删除自己的评论
    - 管理员或文章作者可以删除任何评论（但通常不修改他人评论）
    - 其他人只读
    """
    def has_object_permission(self, request, view, obj):
        # 读取方法允许所有请求
        if request.method in permissions.SAFE_METHODS:
            return True

        # 评论作者本人可以修改/删除
        if obj.author == request.user:
            return True

        # 管理员或文章作者可以删除（但通常不允许修改）
        if request.method == 'DELETE':
            if request.user.is_staff or obj.article.author == request.user:
                return True

        return False