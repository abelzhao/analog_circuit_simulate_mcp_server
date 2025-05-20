# ngspice-mcp-server

ngspice电路仿真的模型上下文协议(MCP)服务器

## 功能特性

- 提供运行ngspice仿真的MCP工具
- 用于仿真控制的REST API接口
- 支持参数化电路仿真
- 以JSON格式返回仿真结果

## 安装指南

1. 确保已安装Python 3.8+ (参见.python-version文件)
2. 安装依赖:
   ```bash
   pip install -e .
   ```
3. 安装ngspice(仿真后端必需):
   ```bash
   sudo apt-get install ngspice  # Debian/Ubuntu系统
   ```

## 使用说明

### 启动服务器

运行MCP服务器:
```bash
python -m ngspice_mcp_server
```

### API调用示例

使用电路文件运行仿真:
```bash
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{"circuit": "high_pass_filter.cir"}'

#### 响应格式
成功仿真响应:
```json
{
  "status": "completed",
  "results": {
    "vout": [0.0, 0.5, 1.0, ...],
    "frequency": [10, 100, 1000, ...]
  },
  "metadata": {
    "simulation_time": "0.45s",
    "circuit": "high_pass_filter.cir"
  }
}
```

### 配置选项

服务器配置可在`src/ngspice-mcp-server/server.py`中修改:
- 端口号
- 日志级别
- 仿真超时设置

### 客户端配置

从客户端应用连接MCP服务器的配置方法:

1. 安装MCP客户端库:
```bash
pip install model-context-protocol
```

2. 配置服务器URL(默认为http://localhost:8000):
```python
from mcp import MCPClient

client = MCPClient(server_url="http://localhost:8000")
```

3. 运行仿真实例:
```python
response = client.use_tool(
    tool_name="simulate",
    arguments={"circuit": "high_pass_filter.cir"}
)
print(response["results"])
```

可通过环境变量配置:
- `MCP_SERVER_URL`: 覆盖默认服务器URL
- `MCP_API_KEY`: 设置认证密钥(如需)

## 开发指南

### 项目结构

- `src/ngspice-mcp-server/` - 主包源代码
  - `server.py` - MCP服务器实现
  - `simulate.py` - 仿真逻辑
  - `__main__.py` - CLI入口点
- `high_pass_filter.cir` - 示例电路
- `pyproject.toml` - Python项目配置

### 测试

运行测试套件:
```bash
pytest
```

## 许可证

MIT许可证

特此免费授予任何获得本软件及相关文档文件(以下简称"软件")副本的人，不受限制地处理本软件，包括但不限于使用、复制、修改、合并、发布、分发、再许可和/或销售本软件的副本，并允许接受本软件的人这样做，但须符合以下条件:

上述版权声明和本许可声明应包含在本软件的所有副本或主要部分中。

本软件按"原样"提供，不作任何明示或暗示的保证，包括但不限于对适销性、特定用途适用性和非侵权性的保证。在任何情况下，作者或版权持有人均不对任何索赔、损害或其他责任负责，无论是在合同诉讼、侵权行为或其他方面，由本软件或本软件的使用或其他交易引起、与之相关或与之相关的。
