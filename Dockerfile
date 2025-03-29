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
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Fix entrypoint.sh file permissions and format
RUN dos2unix /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Fix check_services.sh file permissions
RUN chmod +x /app/check_services.sh

# Set the default command
CMD ["/bin/bash", "/app/entrypoint.sh"]

