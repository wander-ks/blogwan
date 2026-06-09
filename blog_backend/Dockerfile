FROM python:3.8-slim 

# 3.8必须安装的编译依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    python3-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装 Python 依赖（清华源）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple
    
COPY . .
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

# 启动命令将在 docker-compose 中覆盖（以便执行 migrate）
CMD ["gunicorn", "blog_backend.wsgi:application", "--bind", "0.0.0.0:8080"]