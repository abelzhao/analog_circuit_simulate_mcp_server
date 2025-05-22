import contextlib
import logging
import click
from collections.abc import AsyncIterator

from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
import mcp.types as mcp_types


from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send

from .simulate import ngspice_simulate

@click.command()
@click.option('--port', type=int, default=4044, help='Port to run the server on')
@click.option('--log-level', type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']), 
        default='info', help='Logging level')
@click.option('--json-response', is_flag=True, default=True, help='Return responses in JSON format')
def main(port, log_level, json_response):
    # 设置logging配置参数
    logging.basicConfig(level=log_level.upper(), 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("ngspice-mcp-server")
    logger.info("Starting ngspice-mcp-server...")
    logger.info(f"Server running on port {port}")
    logger.info(f"Log level: {log_level}")
    logger.info(f"JSON response: {json_response}")
    
    # 创建mcp服务
    app = Server("ngspice-mcp-server")
    
    # 请求函数
    @app.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[mcp_types.TextContent]:
        ctx = app.request_context
        circuit = arguments.get("circuit")
        if not circuit:
            raise ValueError("Circuit not provided")
        # send init log message
        await ctx.session.send_log_message(
            level="info",
            data=f"Simulating circuit: \n {circuit}...",
            related_request_id=ctx.request_id
        )
        # simulate circuit
        try:
            
            logger.info(f"request circuit:\n {circuit}")

            result = await ngspice_simulate(circuit)

            logger.info(f"response simulation:\n {result}")

            if result["status"] == "success":
                await ctx.session.send_log_message(
                    level="info",
                    data=f"Simulation successful: {result['message']}",
                    related_request_id=ctx.request_id
                )
                return [mcp_types.TextContent(type='text', text=result["message"])]
            else:
                await ctx.session.send_log_message(
                    level="error",
                    data=f"Simulation failed: {result['message']}",
                    related_request_id=ctx.request_id
                )
                return [mcp_types.TextContent(type='text', text=result["message"])]
        except Exception as e:
            await ctx.session.send_log_message(
                level="error",
                data=f"Error simulating circuit: {str(e)}",
                related_request_id=ctx.request_id
            )
            raise
        
    @app.list_tools()
    async def handle_list_tools() -> list[mcp_types.Tool]:
        """List all tools available in the server."""
        return [
            mcp_types.Tool(
                name="ngspice_simulate",
                description="对SPICE电路文件进行仿真",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "circuit": {
                            "type": "string",
                            "description": "SPICE电路文件内容"
                        }
                    },
                    "required": ["circuit"]
                }
            )
        ]
    
    # http session manager
    session_manager = StreamableHTTPSessionManager(
        app=app,
        event_store=None,
        json_response=json_response,
        stateless=True,
    )
    
    async def handle_streamable_http(scope: Scope, receive: Receive, send: Send) -> None:
        await session_manager.handle_request(scope, receive, send)
        
    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        """Context manager for session manager."""
        async with session_manager.run():
            logger.info("Ngspice Mcp Server Started!")
            try:
                yield
            finally:
                logger.info("Ngspice Mcp Server shutting down...")

    # Create an ASGI application using the transport
    starlette_app = Starlette(
        debug=False,
        routes=[
            Mount("/mcp", app=handle_streamable_http),
        ],
        lifespan=lifespan,
    )
    
    import uvicorn

    uvicorn.run(starlette_app, host="0.0.0.0", port=port)

    return 0

if __name__ == "__main__":
    main()
