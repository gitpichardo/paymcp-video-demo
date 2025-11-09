#!/usr/bin/env python3
"""
Railway deployment wrapper that sets HOST=0.0.0.0 before importing FastMCP.
"""
import os
import sys

# Set HOST and PORT BEFORE importing anything else
# This ensures FastMCP picks them up when it initializes
os.environ["HOST"] = "0.0.0.0"
os.environ["PORT"] = os.getenv("PORT", "8000")

# Now import and run the server
if __name__ == "__main__":
    # Import the server module (this creates the mcp instance)
    import server
    
    # Run the FastMCP server
    server.mcp.run(transport="streamable-http")

