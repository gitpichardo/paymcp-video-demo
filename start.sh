#!/bin/bash
# Railway startup script
# Sets HOST=0.0.0.0 before Python starts

export UVICORN_HOST=0.0.0.0
export UVICORN_PORT=${PORT:-8000}
export HOST=0.0.0.0

exec python3 run.py

