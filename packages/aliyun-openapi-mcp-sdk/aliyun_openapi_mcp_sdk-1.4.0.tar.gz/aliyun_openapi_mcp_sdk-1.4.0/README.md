# aliyun-openapi-mcp-sdk

A zero-configuration tool for integrating Model Context Protocol (MCP) servers with any OpenAPI-compliant application.

[![PyPI version](https://badge.fury.io/py/aliyun-openapi-mcp-sdk.svg)](https://pypi.org/project/aliyun-openapi-mcp-sdk/)
[![Python Versions](https://img.shields.io/pypi/pyversions/aliyun-openapi-mcp-sdk.svg)](https://pypi.org/project/aliyun-openapi-mcp-sdk/)

## Features

- **Magical integration** - Instantly create an MCP server from any OpenAPI specification with zero configuration
- **Automatic discovery** - All API endpoints are automatically converted to MCP tools
- **Documentation preservation** - API documentation is automatically converted to MCP tool descriptions
- **Framework agnostic** - Works with any API framework that supports OpenAPI (FastAPI, Flask, Django, etc.)
- **Zero manual setup** - No need to create MCP tools manually, everything is done automatically

## Installation

We recommend using [uv](https://docs.astral.sh/uv/), a fast Python package installer:

```bash
uv add aliyun-openapi-mcp-sdk
```

Alternatively, you can install with pip:

```bash
pip install aliyun-openapi-mcp-sdk
```

## Basic Usage

The simplest way to use OpenAPI-MCP is to point it at your OpenAPI specification:

```python
from aliyun_openapi_mcp_sdk import create_mcp_server, serve_mcp

# Just point it at your OpenAPI spec and it does everything automatically
serve_mcp(
    create_mcp_server("https://your-api.com/openapi.json"),
    host="127.0.0.1", 
    port=8000
)

# That's it! Your MCP server is now running with all API endpoints available as tools
```

If you're using FastAPI, it's even easier:

```python
from fastapi import FastAPI
from aliyun_openapi_mcp_sdk import add_mcp_server

# Your FastAPI app
app = FastAPI()

# Add some endpoints
@app.get("/hello/{name}")
async def hello(name: str):
    """Say hello to someone"""
    return {"message": f"Hello, {name}!"}

# One line to add an MCP server - everything is automatic!
add_mcp_server(app, mount_path="/mcp")

# That's it! Your auto-generated MCP server is now available at `https://app.base.url/mcp`
```

OpenAPI-MCP is framework-agnostic and works with any API that has an OpenAPI specification:

```python
# Flask with OpenAPI spec
from flask import Flask
from aliyun_openapi_mcp_sdk import create_mcp_server, serve_mcp

# Use your existing OpenAPI specification from any framework
openapi_url = "http://your-flask-app.com/swagger.json"  # URL to your OpenAPI spec

# Create the MCP server from the OpenAPI spec
mcp_server = create_mcp_server(openapi_url)

# Serve the MCP server
serve_mcp(mcp_server, host="127.0.0.1", port=8000)
```

## How It Works

1. OpenAPI-MCP reads your OpenAPI specification
2. It automatically discovers all endpoints and their parameters
3. It automatically converts each endpoint into an MCP tool
4. It automatically generates descriptions, schemas, and examples for each tool
5. It automatically handles HTTP requests to your API when tools are called

No manual tool creation, no boilerplate code, no configuration needed!

## Examples

### OpenAPI Specification Example:

```python
from aliyun_openapi_mcp_sdk import create_mcp_server, serve_mcp

# Just point it at any OpenAPI specification URL
mcp_server = create_mcp_server("https://api.example.com/openapi.json")

# Start the server
if __name__ == "__main__":
    serve_mcp(mcp_server, host="127.0.0.1", port=8000)
```

### Framework-Specific Examples

#### FastAPI Example:

```python
from fastapi import FastAPI
from aliyun_openapi_mcp_sdk import add_mcp_server

app = FastAPI(title="Simple API")

@app.get("/hello/{name}")
async def hello(name: str):
    """Say hello to someone"""
    return {"message": f"Hello, {name}!"}

# Just one line to add an MCP server - no configuration needed!
add_mcp_server(app, mount_path="/mcp")
```

## Connecting to the MCP Server

Once your MCP server is running, you can connect to it with any MCP client, such as Claude:

1. Run your application
2. In Claude, use the URL of your MCP server endpoint (e.g., `http://localhost:8000/mcp`)
3. Claude will discover all available tools and resources automatically

## Advanced Options (Optional)

While OpenAPI-MCP is designed to work automatically with zero configuration, there are a few optional settings available if you need more control:

```python
from aliyun_openapi_mcp_sdk import create_mcp_server, serve_mcp

# Create the MCP server with optional customizations
mcp_server = create_mcp_server(
    "https://your-api.com/openapi.json",
    name="My Custom API MCP",                        # Custom name for the MCP server
    base_url="https://your-api.com",                 # Base URL for API requests
    describe_all_responses=True,                     # Include error response schemas in tool descriptions
    describe_full_response_schema=True,              # Include detailed response schemas
)

# You can also register custom functions directly with the MCP server
from mcp.types import ToolDefinition

def get_server_time() -> str:
    """Get the current server time."""
    from datetime import datetime
    return datetime.now().isoformat()

# Register the function as a tool
mcp_server.register_tool(
    ToolDefinition(
        name="get_server_time",
        description="Get the current server time.",
        implementation=get_server_time
    )
)

# Serve the MCP server
serve_mcp(mcp_server, host="127.0.0.1", port=8000)
```

## Requirements

- Python 3.7+
- uv

## License

MIT License. Copyright (c) 2024 Tadata Inc.

## About

Developed and maintained by [Tadata Inc.](https://github.com/aliyun)
