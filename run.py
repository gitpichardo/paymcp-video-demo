#!/usr/bin/env python3
"""
Railway deployment wrapper that monkey-patches uvicorn to bind to 0.0.0.0.
"""
import os
import sys

# Monkey-patch uvicorn.run to force host=0.0.0.0
import uvicorn
_original_run = uvicorn.run

def patched_run(app, **kwargs):
    """Patched uvicorn.run that forces host=0.0.0.0 for Railway."""
    kwargs['host'] = '0.0.0.0'
    kwargs['port'] = int(os.getenv("PORT", kwargs.get('port', 8000)))
    print(f"[Patched] Starting uvicorn on {kwargs['host']}:{kwargs['port']}", file=sys.stderr)
    return _original_run(app, **kwargs)

uvicorn.run = patched_run

# Now import and run the server
if __name__ == "__main__":
    # Import the server module (this creates the mcp instance)
    import server
    
    # Run the FastMCP server (will use our patched uvicorn.run)
    server.mcp.run(transport="streamable-http")

