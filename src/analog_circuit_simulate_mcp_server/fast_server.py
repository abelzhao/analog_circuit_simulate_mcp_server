import logging
import click
from mcp.server.fastmcp import FastMCP
from .simulate import ngspice_simulate

@click.command()
@click.option('--log-level', default='info', type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']), help='Set the logging level')
def main(log_level):
    # 设置logging配置参数
    logging.basicConfig(level=log_level.upper(), 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("ngspice-mcp-server")
    logger.info("Starting ngspice-mcp-server...")

    # 构建mcp
    mcp = FastMCP("ngspice-mcp-server", dependencies=["pyautogui", "Pillow"])

    # 请求函数
    @mcp.tool(description="调用仿真器进行电路仿真")
    async def simulate(circuit: str, simulator:str = 'ngspice', option:str = '-b') -> str:
        """调用仿真器进行电路仿真
        Args:
            circuit (str): 需要仿真的SPICE电路.
            simulator (str): 仿真器名称. 默认是ngspice. 目前只支持ngspice.
            option (str): ngspice的选项. 默认是-b, 批处理模式.
        Returns:
            str: 仿真结果.
        """
        if simulator != "ngspice":
            raise ValueError(f"Unsupported simulator: {simulator}. Only ngspice is supported.")
        logging.debug(f"request circuit:\n {circuit}")
        result = await ngspice_simulate(circuit, option)
        if result["status"] == "success":
            logging.debug(f"response simulation:\n {result}")
            return result["message"]
        else:
            raise ValueError(result["message"])

    mcp.run(transport="streamable-http")
