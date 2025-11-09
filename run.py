#!/usr/bin/env python3
"""
Railway deployment wrapper that sets uvicorn host=0.0.0.0.
"""
import os
import sys

# Set uvicorn-specific environment variables
# UVICORN_HOST is what uvicorn actually reads
os.environ["UVICORN_HOST"] = "0.0.0.0"
os.environ["UVICORN_PORT"] = os.getenv("PORT", "8000")

# Also set these for good measure
os.environ["HOST"] = "0.0.0.0"
os.environ["PORT"] = os.getenv("PORT", "8000")

# Now import and run the server
if __name__ == "__main__":
    # Import the server module (this creates the mcp instance)
    import server
    
    # Run the FastMCP server
    server.mcp.run(transport="streamable-http")

