import subprocess
import os
import sys
import tempfile
import shutil
import logging
from typing import Optional
from pathlib import Path

def ngspice_simulate(
    circuit: str
) -> dict:
    """
    Simulate a circuit using ngspice.

    Args:
        circuit (str): The circuit to simulate.

    Returns:
        str: The results of the simulation.
    """
    # 创建临时文件保存电路文件
    with tempfile.NamedTemporaryFile(suffix=".cir", delete=False) as f:
        circuit_name = f.name
        f.write(circuit.encode('utf-8'))
        f.flush()
        os.fsync(f.fileno())
    cmd = ["ngspice", "-b", circuit_name]
    
    try:
        ret = subprocess.run(cmd, 
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            check=False,
                            )
        return {
            "status": "success",
            "message": ret.stdout,
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": e.stderr,
        }

if __name__ == "__main__":
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
    circuit_name = "high_pass_filter.cir"
    
    result = ngspice_simulate(circuit)
    print(result)