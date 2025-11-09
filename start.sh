#!/bin/bash
# Railway startup script

# Use Railway's PORT or default to 8000
PORT=${PORT:-8000}

# Run uvicorn directly with the FastMCP app
# This bypasses FastMCP's run() method and gives us control over host binding
exec python3 -m uvicorn server:app --host 0.0.0.0 --port $PORT

