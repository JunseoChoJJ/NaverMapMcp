import uvicorn
from starlette.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from app.tools.directions import register_directions_tool
from app.tools.geocode import register_geocode_tool
from app.tools.places import register_places_tool

from dotenv import load_dotenv
load_dotenv()


# 나머지 import...
def createMcpServer() -> FastMCP:
    mcp = FastMCP(
        "Supabase MCP Server",
        stateless_http=True,
        json_response=True,
        host="0.0.0.0",
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=False,
        ),
    )
    register_geocode_tool(mcp)
    register_directions_tool(mcp)
    register_places_tool(mcp)
    
    
    return mcp


if __name__ == "__main__":
    mcp = createMcpServer()
    app = mcp.streamable_http_app()

    

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host="0.0.0.0", port=8002)