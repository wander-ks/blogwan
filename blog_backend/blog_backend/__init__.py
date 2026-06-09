import pymysql
pymysql.install_as_MySQLdb()

from blog_backend.celery import app as celery_app

__all__ = ('celery_app',)