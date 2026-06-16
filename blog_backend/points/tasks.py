from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from notifications.models import Message
from points.models import SignInRecord, Festival, UserPoints, UserFestivalReceiveLog
from points.services import update_points
from django.db import transaction
import logging

User = get_user_model()

logger = logging.getLogger(__name__)
BATCH_SIZE = 500

@shared_task
def send_daily_sign_reminder():
    """每天8点向所有用户发送签到提醒站内信"""
    today = timezone.now().date()
    signed_users = SignInRecord.objects.filter(sign_date=today).values_list('user_id', flat=True)
    users = User.objects.exclude(id__in=signed_users)
    total = users.count()
    if total == 0:
        logger.info("今日所有用户已完成签到，无需发送提醒")
        return "No user need sign reminder"

    total_send = 0
    offset = 0
    while True:
        batch_users = list(users[offset:offset + BATCH_SIZE])
        if not batch_users:
            break
        msg_batch = []
        for user in users:
            msg_batch.append(Message(
                recipient=user,
                message_type="system",
                title="每日签到提醒",
                content="今日尚未签到，快点击导航栏“签到”按钮领取积分吧！",
                link="/"
            ))
        Message.objects.bulk_create(msg_batch)
        batch_num = len(msg_batch)
        total_send += batch_num
        logger.info(f"签到提醒批量发送{batch_num}条，累计{total_send}/{total}")
        offset += BATCH_SIZE

    result_msg = f"签到提醒发放完成，总计推送{total_send}位用户"
    logger.info(f"签到提醒发放完成，总计推送{total_send}位用户")
    return result_msg


@shared_task
def check_festival_bonus():
    """检查当天是否有节日，若有则给所有用户发放积分"""
    today = timezone.now()
    month, day = today.month, today.day
    today_date = today.date()
    festivals = Festival.objects.filter(month=month, day=day)
    if not festivals:
        return 'No festival today'

    result_msg = []
    for festival in festivals:
        fid = festival.id
        bonus = festival.bonus_points
        fname = festival.name
        received_uids = UserFestivalReceiveLog.objects.filter(
            festival_id=fid,
            receive_date=today_date
        ).values_list("user_id", flat=True)

        target_qs = User.objects.exclude(id__in=received_uids)
        total_target = target_qs.count()
        if total_target == 0:
            tip = f"节日【{fname}】今日全部用户已领取，跳过发放"
            logger.info(tip)
            result_msg.append(tip)
            continue

        send_success = 0
        offset = 0
        while True:
            batch_users = list(target_qs[offset:offset + BATCH_SIZE])
            if not batch_users:
                break
            with transaction.atomic():
                receive_log_batch = []
                for user in batch_users:
                    try:
                        update_points(
                            user=user,
                            amount=bonus,
                            trans_type="festival",
                            related_id=str(fid),
                            description=f"{fname}节日福利"
                        )
                        receive_log_batch.append(UserFestivalReceiveLog(
                            user=user,
                            festival_id=fid
                        ))
                        send_success += 1
                    except Exception as e:
                        logger.error(f"用户{user.id}领取【{fname}】积分失败: {str(e)}", exc_info=True)
                UserFestivalReceiveLog.objects.bulk_create(receive_log_batch)

            logger.info(f"【{fname}】批次发放成功{len(receive_log_batch)}人")
            offset += BATCH_SIZE
        finish_tip = f"节日【{fname}】发放完毕，应发{total_target}人，成功{send_success}人"
        result_msg.append(finish_tip)
        logger.info(finish_tip)

        final_msg = " | ".join(result_msg)
        logger.info(f"当日所有节日处理完成：{final_msg}")
        return final_msg










        users = User.objects.all()
        for user in users:
            update_points(user, festival.bonus_points, 'festival', description=f'{festival.name}福利')
            result_msg.append(f'Festival bonus {festival.bonus_points} points sent to {users.count()} users')