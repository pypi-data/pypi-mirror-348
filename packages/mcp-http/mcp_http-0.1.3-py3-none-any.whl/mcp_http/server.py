# server.py
import string
from fastmcp import FastMCP, Context
from pydantic import Field, HttpUrl
import httpx
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any
# from src.mcp_http.config import security_config
import logging
# Reuse connection pool (performance optimization)
@asynccontextmanager
async def http_client_lifespan(app):
    async with httpx.AsyncClient(
        limits=httpx.Limits(
            max_connections=100,
            max_keepalive_connections=20
        ),
        follow_redirects=True,
    ) as client:
        yield {"client": client}
   

mcp = FastMCP("HTTPProxyService", instructions="Integrated HTTP proxy service supporting GET/POST/PUT/DELETE", dependencies=["httpx"], lifespan=http_client_lifespan)
def _validate_domain(url: str):
    """Domain whitelist validation"""
    return
    # domain = url.split("//")[-1].split("/")[0]
    # if domain not in security_config.allowed_domains:
    #     raise ValueError(f"Access to domain is forbidden: {domain}")

@mcp.tool(name="http_get", description="Execute GET request")
async def http_get(
    ctx: Context,
    url: str = Field(..., description="Target URL, e.g. https://api.example.com/data"),
    params: Optional[Dict[str, Any]] = Field(default=None, description="URL query parameters"),
) -> str:
    _validate_domain(url)
    logging.debug(f"lifespan_context to {ctx}")
    client = ctx.request_context.lifespan_context["client"]
    response = await client.get(url, params=params)
    return f"Status: {response.status_code}\nContent: {response.text}"

@mcp.tool(name="http_post", description="Execute POST request")
async def http_post(
    ctx: Context,
    url: str = Field(...),
    params: Optional[Dict[str, Any]] = Field(default=None, description="URL query parameters"),
    body: Dict[str, Any] = Field(default=None, description="JSON request body"),
    headers: Optional[Dict[str, str]] = Field(
        default={"Content-Type": "application/json"},
        description="Request headers (default includes Content-Type)"
    ),
) -> str:
    _validate_domain(url)
    client = ctx.request_context.lifespan_context["client"]
    response = await client.post(url, params=params,json=body, headers=headers)
    return f"Status: {response.status_code}\nContent: {response.text}"

@mcp.tool(name="http_put", description="Execute PUT request")
async def http_put(
    ctx: Context,
    url: str = Field(...),
    params: Optional[Dict[str, Any]] = Field(default=None, description="URL query parameters"),
    body: Dict[str, Any] = Field(default=None, description="JSON request body"),
    headers: Optional[Dict[str, str]] = Field(
        default={"Content-Type": "application/json"},
        description="Request headers (default includes Content-Type)"
    ),
) -> str:
    _validate_domain(url)
    client = ctx.request_context.lifespan_context["client"]
    response = await client.put(url,params=params, json=body, headers=headers)
    return f"Status: {response.status_code}\nContent: {response.text}"

@mcp.tool(name="http_delete", description="Execute DELETE request")
async def http_delete(
    ctx: Context,
    url: str = Field(...),
    params: Optional[Dict[str, Any]] = Field(default=None, description="URL query parameters"),
) -> str:
    _validate_domain(url)
    client = ctx.request_context.lifespan_context["client"]
    response = await client.delete(url, params=params)
    return f"Status: {response.status_code}"
def run():
    mcp.run(transport='stdio')
    #log_level="debug"
    #  mcp.run(
    #     transport="streamable-http",
    #     host="0.0.0.0",
    #     port=8080,
    #     routes=[("/mcp", mcp)],  # Add route configuration
    #     log_level="debug"  # Enable debug log
    # )

if __name__ == "__main__":
    run()