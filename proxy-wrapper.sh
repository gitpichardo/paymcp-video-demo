#!/bin/bash
# Wrapper script to capture proxy logs for debugging

PROXY_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="/tmp/paymcp-proxy.log"

# Clear old log
> "$LOG_FILE"

# Log startup
echo "=== Proxy started at $(date) ===" >> "$LOG_FILE" 2>&1

# Run proxy and capture stderr to log file
exec node "$PROXY_DIR/proxy.js" 2>> "$LOG_FILE"

