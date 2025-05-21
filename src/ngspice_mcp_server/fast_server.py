import logging
import click
from mcp.server.fastmcp import FastMCP
from .simulate import ngspice_simulate

@click.command()
@click.option('--log-level', default='info', type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']), help='Set the logging level')
@click.option('--json-response', is_flag=True, default=False, help='Return responses in JSON format')
def main(log_level, json_response):
    # 设置logging配置参数
    logging.basicConfig(level=log_level.upper(), 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("ngspice-mcp-server")
    logger.info("Starting ngspice-mcp-server...")
    logger.info(f"Log level: {log_level}")
    logger.info(f"JSON response: {json_response}")

    # 构建mcp
    mcp = FastMCP("ngspice-mcp-server")

    # 请求函数
    @mcp.tool(description="调用ngspice进行电路仿真")
    async def simulate(circuit: str, simulator:str = 'ngspice') -> str:
        """调用ngspice进行电路仿真.
        Args:
            circuit (str): 需要仿真的SPICE电路.
            simulator (str): 仿真器，当前只支持: 'ngspice'.
        Returns:
            str: 仿真结果.
        """
        if simulator != 'ngspice':
            raise ValueError("Unsupported simulator. Only 'ngspice' is supported.")
        
        logging.info(f"request circuit:\n {circuit}")
        result = await ngspice_simulate(circuit)
        if result["status"] == "success":
            logging.info(f"response simulation:\n {result}")
            return result["message"]
        else:
            raise ValueError(result["message"])

    mcp.run(transport="streamable-http")
