# analog-circuit-simulate-mcp-server

A Model Context Protocol (MCP) server for analog circuit simulation

## Features

- Provides MCP tools for running analog circuit simulations
- REST API interface for simulation control
- Supports parameterized circuit simulations
- Returns simulation results in JSON format

## Installation Guide (Linux only)

1. Install ngspice (required for simulation backend):
   ```bash
   sudo apt-get install ngspice  # For Debian/Ubuntu systems
   ```

2. Ensure Python 3.8+ is installed (see .python-version file) and install uv tool:
   ```bash
   pip install uv
   ```

3. Create and activate virtual environment:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # Linux/macOS
   ```

4. Install dependencies using different methods:
   - Direct installation with uv:
     ```bash
     uv pip install -e .
     ```
   - Build with uv then install:
     ```bash
     uv build && pip install dist/analog_circuit_simulate_mcp_server-${version}-py3-none-any.whl
     # or uv build && pip install dist/analog_circuit_simulate_mcp_server-${version}.tar.gz
     ```
   - Traditional pip installation:
     ```bash
     pip install -e .
     ```

## Usage

### Starting the Server
Different ways to run the server:
- Using uv run:
  ```bash
  uv run analog-circuit-simulate-mcp-server
  ```
- Using uvx (requires uvx installation):
  ```bash
  uvx --from https://github.com/abelzhao/analog_circuit_simulate_mcp_server.git ngspice-mcp-server
  ```

### NPX Configuration
```
{
  "mcpServers": {
    "ngspice-mcp-server": {
      "command": "uvx",
      "args": [
        "http://${server_ip}:4044/mcp/"
      ]
    }
  }
}
```

### Configuration Options

Server configuration can be modified in `.venv`:
- FASTMCP_PORT=4044
- FASTMCP_JSON_RESPONSE=True

## Development Guide

# analog-circuit-simulate-mcp-server Project Structure

```
.
├── .gitignore
├── .python-version
├── high_pass_filter.cir         # Example circuit file
├── pyproject.toml              # Python project configuration
├── README.md                   # English documentation
├── README.zh-CN.md             # Chinese documentation
├── uv.lock                     # UV dependency lock file
├── build/                      # Build directory
└── src/                        # Source code directory
    └── analog_circuit_simulate_mcp_server/     # Main package source
        ├── __init__.py         # Package initialization
        ├── __main__.py         # CLI entry point
        ├── server.py           # MCP server implementation
        └── simulate.py         # Simulation logic
```

## File Descriptions

- `high_pass_filter.cir`: Example circuit file for circuit simulation demo
- `src/analog_circuit_simulate_mcp_server/server.py`: Contains MCP server implementation and REST API interface
- `src/analog_circuit_simulate_mcp_server/simulate.py`: Contains circuit simulation logic and result processing
- `pyproject.toml`: Defines Python package metadata, dependencies and build configuration


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


### Testing

Run test suite:
```bash
pytest
```

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
