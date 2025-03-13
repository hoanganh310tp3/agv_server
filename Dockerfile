# Base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
    dnsutils \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Copy entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Copy check_services.sh
COPY check_services.sh /app/
RUN chmod +x /app/check_services.sh

# Run entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"] 