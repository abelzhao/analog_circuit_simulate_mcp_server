# analog-circuit-simulate-mcp-server

模拟电路仿真的模型上下文协议(MCP)服务器

## 功能特性

- 提供运行模拟电路仿真的MCP工具
- 用于仿真控制的REST API接口
- 支持参数化电路仿真
- 以JSON格式返回仿真结果

## 安装指南（只在Linux系统下运行）

1. 安装ngspice(仿真后端必需):
   ```bash
   sudo apt-get install ngspice  # Debian/Ubuntu系统
   ```

2. 确保已安装Python 3.8+ (参见.python-version文件)和uv工具:
   ```bash
   pip install uv
   ```

3. 创建并激活虚拟环境:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # Linux/macOS
   ```

4. 使用不同方式安装依赖:
   - 使用uv直接安装:
     ```bash
     uv pip install -e .
     ```
   - 使用uv build后安装:
     ```bash
     uv build && pip install dist/analog_circuit_simulate_mcp_server-${version}-py3-none-any.whl
     # 或 uv build && pip install dist/analog_circuit_simulate_mcp_server-${version}.tar.gz
     ```
   - 使用传统pip安装:
     ```bash
     pip install -e .
     ```

## 使用说明

### 启动服务器
运行服务器的不同方式:
- 使用uv run运行:
  ```bash
  uv run analog-circuit-simulate-mcp-server
  ```
- 使用uvx运行(需先安装uvx):
  ```bash
  uvx --from https://github.com/abelzhao/analog_circuit_simulate_mcp_server.git  analog-circuit-simulate-mcp-server
  ```

### NPX
```
{
  "mcpServers": {
    "analog-circuit-simulate-mcp-server": {
      "command": "uvx",
      "args": [
        "http://${server_ip}:4044/mcp/"
      ]
    }
  }
}
```




### 配置选项

服务器配置可在`src/ngspice-mcp-server/server.py`中修改:
- FASTMCP_PORT=4044
- FASTMCP_JSON_RESPONSE=True


## 开发指南

# ngspice-mcp-server 项目结构

```
.
├── .gitignore
├── .python-version
├── high_pass_filter.cir         # 示例电路文件
├── pyproject.toml              # Python项目配置
├── README.md                   # 英文文档
├── README.zh-CN.md             # 中文文档
├── uv.lock                     # UV依赖锁定文件
├── build/                      # 构建目录
└── src/                        # 源代码目录
    └── ngspice_mcp_server/     # 主包源代码
        ├── __init__.py         # 包初始化文件
        ├── __main__.py         # CLI入口点
        ├── server.py           # MCP服务器实现
        └── simulate.py         # 仿真逻辑
```

## 文件说明

- `high_pass_filter.cir`: 示例电路文件，用于演示模拟电路仿真
- `src/analog_circuit_simulate_mcp_server/server.py`: 包含MCP服务器实现和REST API接口
- `src/analog_circuit_simulate_mcp_server/simulate.py`: 包含模拟器仿真逻辑和结果处理
- `pyproject.toml`: 定义Python包元数据、依赖和构建配置

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
