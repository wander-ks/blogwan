from django.db import transaction
from django.utils import timezone
from points.models import UserPoints, PointsTransaction
from django.contrib.auth import get_user_model

User = get_user_model()

def update_points(user, amount, trans_type, related_id='', description=''):
    """统一积分变更方法，自动更新余额和流水"""
    with transaction.atomic():
        points, created = UserPoints.objects.select_for_update().get_or_create(user=user, defaults={'balance':0, 'total_earned':0})
        points.balance += amount
        if amount > 0:
            points.total_earned += amount
        points.save()
        PointsTransaction.objects.create(
            user=user,
            amount=amount,
            transaction_type=trans_type,
            related_object_id=related_id,
            description=description
        )
    return points.balance