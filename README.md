# blogwan

blogwan - 博客内容发布平台
blogwan 是一个功能完整的全栈博客系统，支持用户认证、文章管理、评论互动、点赞关注、积分激励、付费下载及站内信通知。后端基于 Django + DRF，前端基于 Vue 3，提供 RESTful API 和现代化的前端界面。

功能特性
用户系统：注册/登录（JWT）、个人资料（头像/简介）、邮箱验证（站内信替代）
文章管理：发布/编辑/删除、分页/搜索/筛选、阅读量统计、封面图上传
评论互动：顶级评论分页、嵌套回复（独立页面）、评论通知
点赞关注：点赞/取消点赞（Redis + 最终一致性）、关注/取关、粉丝推送
积分系统：签到（每日+满月奖励）、发文奖励（+10）、获赞奖励（+2）、付费下载（-1）
站内信：欢迎消息、评论通知、关注作者发文通知、下载链接消息、每日签到提醒
付费下载：支付1积分获取文章下载链接（临时token，有效期1小时）
管理后台：Django Admin 支持内容管理
API文档：Swagger UI + ReDoc 自动生成

技术栈

后端
Python 3.8
Django 4.1
Django REST Framework 3.14
JWT (SimpleJWT)
MySQL 5.7
Redis 7.0 (缓存/消息队列)
Celery 5.3 + Celery Beat
Gunicorn

前端
Vue 3 + Vite
Vue Router 4
Axios
Bootstrap 5
Day.js

部署与运维
Docker + Docker Compose
Nginx
Sealos (Kubernetes)
Git

启动 Celery（可选）
celery -A blog_backend worker --loglevel=info             # 异步任务 Linux
celery -A blog_backend worker --loglevel=info -P eventlet # 异步任务 windows
celery -A blog_backend beat --loglevel=info               # 定时任务（可选）

API 文档：http://localhost/api/v1/schema/swagger-ui/
