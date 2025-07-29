
import asyncio
from fastmcp import FastMCP
from .server import io_mcp, pp_mcp, tl_mcp, pl_mcp, ul_mcp
import liana_mcp.server as limcp

sc_mcp = FastMCP("Scanpy-MCP-Server")


async def setup():
    await sc_mcp.import_server("io", io_mcp)
    await sc_mcp.import_server("pp", pp_mcp)
    await sc_mcp.import_server("tl", tl_mcp) 
    await sc_mcp.import_server("pl", pl_mcp) 
    await sc_mcp.import_server("ul", ul_mcp)

    

if __name__ == "__main__":
    asyncio.run(setup())
    sc_mcp.run()
