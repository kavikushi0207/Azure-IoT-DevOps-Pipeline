FROM python:3.10-slim

WORKDIR /app

# Install all necessary compilation tools and cryptographic headers
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first, then install requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python scripts into the container
COPY sensor_producer.py .
COPY edge_gateway.py .