import asyncio
import os
import tempfile


async def ngspice_simulate(
    circuit: str,
    option: str = "-b",
) -> dict:
    """
    Simulate a circuit using ngspice.

    Args:
        circuit (str): The circuit to simulate.
        option (str): The ngspice option to use. Default is "-b" for batch mode.

    Returns:
        str: The results of the simulation.
    """
    # 创建临时文件保存电路文件
    
    
    try:
        with tempfile.NamedTemporaryFile(suffix=".cir", delete=False) as f:
            circuit_name = f.name
            f.write(circuit.encode('utf-8'))
            f.flush()
            os.fsync(f.fileno())
            cmd = ["ngspice", option, circuit_name]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stderr=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            return {
                "status": "success",
                "message": stdout.decode('utf-8'),
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e).encode('utf-8'),
        }

async def test():
    # Example usage
    circuit = """
* High Pass Filter Circuit
* Cutoff frequency: 1/(2*pi*R*C) = ~1.59kHz

* Input voltage source
V1 in 0 SIN(0 1 1k) AC 1

* High pass filter components
R1 in out 1k
C1 out 0 0.1uF

* Analysis commands
.tran 0.1ms 5ms
.print tran v(in) v(out)
.ac dec 10 10 100k
.print ac vdb(out) vp(out)
.end
"""
    result = await ngspice_simulate(circuit)
    print(result)

if __name__ == "__main__":
    asyncio.run(test())
