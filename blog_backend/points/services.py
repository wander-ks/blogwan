from django.db import transaction
from points.models import UserPoints, PointsTransaction
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger(__name__)

User = get_user_model()

def update_points(user, amount, trans_type, related_id='', description=''):
    """
    统一积分变更接口，保证原子性并记录流水。
    返回变更后的余额。
    """
    if amount == 0:
        logger.warning(f"用户{user.id}积分变动值为0，跳过操作")
        return None

    with transaction.atomic():
        points, created = UserPoints.objects.select_for_update().get_or_create(user=user, defaults={'balance':0, 'total_earned':0})
        new_balance = points.balance + amount
        if new_balance < 0:
            raise ValueError(f"用户{user.id}积分不足，当前余额{points.balance}，扣除{abs(amount)}失败")
        points.balance = new_balance
        if amount > 0:
            points.total_earned += amount
        points.save(update_fields=["balance", "total_earned"])
        PointsTransaction.objects.create(
            user=user,
            amount=amount,
            transaction_type=trans_type,
            related_object_id=related_id,
            description=description
        )
        return points.balance