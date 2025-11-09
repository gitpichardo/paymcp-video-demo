#!/bin/bash
# Railway startup script that sets HOST before starting Python

# Export HOST to make uvicorn bind to all interfaces
export HOST=0.0.0.0

# Use Railway's PORT or default to 8000
export PORT=${PORT:-8000}

# Start the server
exec python3 server.py

