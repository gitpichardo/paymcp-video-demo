#!/bin/bash
# Railway startup script

# Just run the server normally
# Railway's internal networking should handle the connection
# even if the server binds to 127.0.0.1
exec python3 server.py

