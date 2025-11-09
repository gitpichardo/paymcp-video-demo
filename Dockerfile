FROM python:3.12-slim

WORKDIR /app

# Install socat for port forwarding (0.0.0.0 -> 127.0.0.1)
RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server.py .
COPY start.sh .
COPY providers/ ./providers/
COPY web/dist/ ./web/dist/

# Make start script executable
RUN chmod +x start.sh

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Start the server with wrapper script that sets HOST=0.0.0.0
CMD ["./start.sh"]

