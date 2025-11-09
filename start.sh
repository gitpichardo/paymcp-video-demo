#!/bin/bash
# Railway startup script with reverse proxy

PORT=${PORT:-8000}

# Start the FastMCP server in background (binds to 127.0.0.1:8000)
python3 server.py &
SERVER_PID=$!

# Give it a moment to start
sleep 2

# Start socat to proxy 0.0.0.0:PORT -> 127.0.0.1:8000
# This allows Railway's external traffic to reach the internal server
exec socat TCP-LISTEN:$PORT,bind=0.0.0.0,fork,reuseaddr TCP:127.0.0.1:8000

