FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/logs /app/cache /app/data

# Copy application files
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CONFIG_PATH=/app/configs/config.docker.yaml

# Expose API port
EXPOSE 8000

# Run the application
CMD ["python", "server.py", "--config", "/app/configs/config.docker.yaml"] 