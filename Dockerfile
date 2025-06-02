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
EXPOSE 8048

# 启动命令
CMD ["uvicorn", "analog_circuit_simulate_mcp_server.fast_server:main", "--host", "0.0.0.0", "--port", "8048"]
