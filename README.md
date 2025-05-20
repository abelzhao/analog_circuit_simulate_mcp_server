# ngspice-mcp-server

A Model Context Protocol (MCP) server for ngspice circuit simulation.

## Features

- Provides MCP tools for running ngspice simulations
- REST API interface for simulation control
- Supports parameterized circuit simulations
- Returns simulation results in JSON format

## Installation

1. Ensure you have Python 3.8+ installed (see .python-version)
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Install ngspice (required for simulation backend):
   ```bash
   sudo apt-get install ngspice  # For Debian/Ubuntu
   ```

## Usage

### Running the Server

Start the MCP server:
```bash
python -m ngspice_mcp_server
```

### Example API Calls

Run a simulation with a circuit file:
```bash
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{"circuit": "high_pass_filter.cir"}'

#### Response Format
Successful simulation response:
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

### Configuration

Server configuration can be modified in `src/ngspice-mcp-server/server.py`:
- Port number
- Logging level
- Simulation timeout

### Client Configuration

To connect to the MCP server from a client application:

1. Install the MCP client library:
```bash
pip install model-context-protocol
```

2. Configure the server URL (default is http://localhost:8000):
```python
from mcp import MCPClient

client = MCPClient(server_url="http://localhost:8000")
```

3. Example usage to run a simulation:
```python
response = client.use_tool(
    tool_name="simulate",
    arguments={"circuit": "high_pass_filter.cir"}
)
print(response["results"])
```

Environment variables can be used for configuration:
- `MCP_SERVER_URL`: Override the default server URL
- `MCP_API_KEY`: Set authentication key if required

## Development

### Project Structure

- `src/ngspice-mcp-server/` - Main package source
  - `server.py` - MCP server implementation
  - `simulate.py` - Simulation logic
  - `__main__.py` - CLI entry point
- `high_pass_filter.cir` - Example circuit
- `pyproject.toml` - Python project configuration

### Testing

Run the test suite:
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
