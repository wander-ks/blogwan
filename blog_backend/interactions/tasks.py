from django.db.models import F
from articles.models import Article
from django_redis import get_redis_connection
from celery import shared_task
import logging
import json

logger = logging.getLogger(__name__)
conn = get_redis_connection('default')
@shared_task
def sync_likes_from_redis():
    """
    定时任务（每5分钟）将 Redis 中缓存的点赞增量同步到 MySQL。
    """

    TASK_LOCK_KEY = "lock_sync_article_likes_task"
    LOCK_EXPIRE = 300
    lock_acquired = conn.set(TASK_LOCK_KEY, "running", ex=LOCK_EXPIRE, nx=True)
    if not lock_acquired:
        logger.warning("点赞同步任务已在运行，本次任务直接退出")
        return "Task skip: already running"
    article_incr_map = {}
    cursor = 0
    updated = 0
    try:
        while True:
            cursor, keys = conn.scan(
                cursor=cursor,
                match="article_like_count_*",
                count=100
            )
            for key in keys:
                try:
                    key_str = key.decode("utf-8")
                    article_id_str = key_str.split("_")[-1]
                    article_id = int(article_id_str)

                    count_bytes = conn.get(key)
                    if not count_bytes:
                        conn.delete(key)
                        continue

                    incr_count = int(count_bytes)
                    if incr_count <= 0:
                        conn.delete(key)
                        continue

                    if article_id in article_incr_map:
                        article_incr_map[article_id] += incr_count
                    else:
                        article_incr_map[article_id] = incr_count
                    conn.delete(key)

                except (ValueError, IndexError) as e:
                    logger.error(f"解析Key失败，key: {key}, 错误: {str(e)}")
                    conn.delete(key)
                    continue
                except Exception as e:
                    logger.error(f"处理Key异常，key: {key}", exc_info=True)
                    conn.delete(key)
                    continue
            if cursor == 0:
                break

        if article_incr_map:
            for aid, num in article_incr_map.items():
                try:
                    Article.objects.filter(id=aid).update(likes=F("likes") + num)
                    updated += 1
                except Exception as e:
                    logger.error(f"文章ID:{aid} 点赞更新失败", exc_info=True)
                    continue
            logger.info(f"点赞同步完成，成功更新 {updated} 篇文章")
        else:
            logger.info("暂无点赞增量数据，无需同步")

        return f"同步完成，共更新 {updated} 个文章的点赞计数"

    except Exception as e:
        logger.error("点赞同步任务整体异常中断", exc_info=True)
        raise
    finally:
        conn.delete(TASK_LOCK_KEY)




@shared_task
def batch_save_like_relations():
    """
    批量保存点赞关系明细
    """
    from django.db import IntegrityError
    from interactions.models import ArticleLike
    LIKE_QUEUE_KEY = "articleLike_article_like_data"
    BATCH_SIZE = 200
    created = 0
    while True:
        raw_list = conn.rpop(LIKE_QUEUE_KEY, BATCH_SIZE)
        if not raw_list:
            logger.info("点赞队列为空，任务结束")
            break

        data_list = []
        for raw in raw_list:
            try:
                data = json.loads(raw.decode("utf-8"))
                data_list.append(data)
            except Exception as e:
                logger.error(f"解析队列数据失败: {raw}, 错误: {e}")
                continue

        for item in data_list:
            try:
                ArticleLike.objects.create(**item)
                created += 1
            except IntegrityError:
                continue
            except Exception as e:
                logger.error(f"保存点赞记录失败: {item}, 错误: {e}", exc_info=True)
                continue

    logger.info(f"批量点赞明细保存完成，本次新增 {created} 条记录")
    return f"成功入库 {created} 条点赞数据"
