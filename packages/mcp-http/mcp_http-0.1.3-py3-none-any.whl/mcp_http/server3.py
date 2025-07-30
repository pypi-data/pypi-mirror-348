# src/http_mcp_server/server.py
from fastmcp import FastMCP
from pydantic import Field
import httpx

mcp = FastMCP("HTTPProxyServer")

@mcp.tool(name="http_request", description="General HTTP request tool supporting GET/POST/PUT/DELETE")
async def http_request(
    method: str = Field(enum=["GET", "POST", "PUT", "DELETE"], description="HTTP method"),
    url: str = Field(description="Target URL, e.g. https://www.baidu.com"),
    params: dict = Field(default={}, description="URL query parameters"),
    headers: dict = Field(default={}, description="Request headers"),
    body: dict = Field(default={}, description="Request body (only for POST/PUT)")
) -> str:
    """Perform an HTTP request and return the response text (handles timeout and exceptions automatically)"""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.request(
            method=method.upper(),
            url=url,
            params=params,
            headers=headers,
            json=body if method in ["POST","PUT"] else None
        )
        return response.text if response.status_code == 200 else f"Error: {response.status_code}"
    
if __name__ == "__main__":
    # Start the server using stdio transport
    mcp.run(transport="stdio")