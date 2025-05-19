import contextlib
import logging
import os
import sys
import time
import anyio
import click

from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import Recieve, Scope, Send


from simulate import ngspice_simulate




@click.command()
@click.option('--port', type=int, default=8000, help='Port to run the server on')
@click.option('--api-key', type=str, required=True, help='API key for authentication')
@click.option('--log-level', type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']), 
              default='info', help='Logging level')
@click.option('--json-response', is_flag=True, default=True, help='Return responses in JSON format')
def main(port, api_key, log_level, json_response):
    # 设置logging配置参数
    logging.basicConfig(level=log_level.upper(), 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("ngspice-mcp-server")
    logger.info("Starting ngspice-mcp-server...")
    logger.info(f"Server running on port {port}")
    logger.info(f"API key: {api_key}")
    logger.info(f"Log level: {log_level}")
    logger.info(f"JSON response: {json_response}")
    
    # 创建mcp服务
    server = Server("ngspice-mcp-server",)


if __name__ == "__main__":
    main()
