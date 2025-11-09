FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server.py .
COPY start.sh .
COPY providers/ ./providers/

# Make start script executable
RUN chmod +x start.sh

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Start the server with wrapper script that sets HOST=0.0.0.0
CMD ["./start.sh"]

