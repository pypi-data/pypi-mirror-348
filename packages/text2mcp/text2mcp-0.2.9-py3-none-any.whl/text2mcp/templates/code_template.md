---
template_name: default_code_template
author: Text2MCP Team
version: 1.0.0
created_at: 2024-05-30
---

# MCP Code Template

## Import Section

```python
import argparse
import logging
import uvicorn
import time
from fastapi.responses import JSONResponse
from mcp.server import FastMCP, Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount
```

## Service Initialization

```python
# Create MCP service
mcp = FastMCP("{{service_name}}")

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```

## MCP Tool Functions

```python
@mcp.tool()
async def {{tool_name}}(param1: str, param2: int = 0):
    """
    {{tool_description}}
    :param param1: {{param1_description}}
    :param param2: {{param2_description}}
    :return: {{return_description}}
    """
    # Implement business logic
    logger.info(f"Request received: param1={param1}, param2={param2}")
    
    # Implementation example
    result = f"Processing result: {param1} - {param2}"
    
    return result
```

## Health Check Endpoint

```python
async def health_check(request):
    """Health check endpoint"""
    return JSONResponse({"status": "healthy", "timestamp": int(time.time())})
```

## Server Creation Function

```python
def create_starlette_app(mcp_server: Server, *, debug: bool = False):
    """Create a Starlette application that provides MCP service"""
    sse = SseServerTransport("/messages/")
    
    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )
    
    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
            Route("/sse/health", endpoint=health_check, methods=["GET"])
        ],
    )
```

## Main Function

```python
if __name__ == "__main__":
    mcp_server = mcp._mcp_server

    parser = argparse.ArgumentParser(description='Run MCP SSE server')
    parser.add_argument("--host", default="0.0.0.0", help="Server host")
    parser.add_argument("--port", default=12345, type=int, help="Server port")
    args = parser.parse_args()
 
    starlette_app = create_starlette_app(mcp_server, debug=True)
    uvicorn.run(starlette_app, host=args.host, port=args.port)
``` 
