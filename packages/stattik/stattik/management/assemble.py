import os
import shutil
import asyncio

from pathlib import Path

from stattik.assembly.assembler import Assembler


async def assemble():
    assembler = Assembler()
    await assembler.assemble()

if __name__ == "__main__":
    asyncio.run(assemble())
