#!/bin/bash
# Railway startup script
# Run uvicorn directly with explicit host binding

PORT=${PORT:-8000}

# Run uvicorn pointing to the asgi_app in server.py
exec python3 -m uvicorn server:asgi_app --host 0.0.0.0 --port $PORT

