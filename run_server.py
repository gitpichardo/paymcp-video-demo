#!/usr/bin/env python3
"""
Custom server runner for Railway deployment.
Runs FastMCP server with explicit host=0.0.0.0 binding.
"""
import os
import sys

# Import the mcp instance from server
from server import mcp

if __name__ == "__main__":
    # Get port from environment
    port = int(os.getenv("PORT", "8000"))
    
    # Import uvicorn
    import uvicorn
    
    # Create the FastMCP HTTP application
    # FastMCP creates an ASGI app internally when using streamable-http
    from fastmcp.server.http import create_http_app
    from mcp.server.fastmcp.server import _make_request_handlers
    
    # Get the request handlers from FastMCP
    handlers = _make_request_handlers(mcp._mcp)
    
    # Create HTTP app with explicit host binding
    app = create_http_app(handlers)
    
    print(f"Starting FastMCP server on 0.0.0.0:{port}", file=sys.stderr)
    
    # Run uvicorn with explicit host and port
    uvicorn.run(app, host="0.0.0.0", port=port)

