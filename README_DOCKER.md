# Docker 部署指南

## 已配置的Docker文件

1. **Dockerfile**
```dockerfile
# 使用官方Python 3.11镜像
FROM python:3.11

# 安装ngspice
RUN apt-get update && apt-get install -y ngspice && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY pyproject.toml .
COPY src/ ./src/

# 安装依赖
RUN pip install --upgrade pip && \
    pip install -e .

# 暴露端口
EXPOSE 8043

# 启动命令
CMD ["uvicorn", "analog_circuit_simulate_mcp_server.fast_server:main", "--host", "0.0.0.0", "--port", "8043"]
```

2. **docker-compose.yml**
```yaml
version: '3.8'

services:
  analog-circuit-simulate:
    build: .
    ports:
      - "8043:8043"
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - .:/app
```

## 部署步骤

1. 构建并启动容器：
```bash
docker-compose up --build
```

2. 服务将在以下地址可用：
http://localhost:8043

3. 停止服务：
```bash
docker-compose down
```

## 注意事项
- 确保系统已安装Docker和docker-compose
- 首次构建可能需要较长时间下载依赖
- 查看日志使用：`docker-compose logs -f`
