FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server.py .
COPY providers/ ./providers/

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Start the server
CMD ["python3", "server.py"]

