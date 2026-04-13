# Start with your exact Python version
FROM python:3.10-slim

# Prevent Python from buffering logs (important for seeing Docker logs)
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Install system helpers for MySQL and Redis
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install your Python libraries
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code into the container
COPY . /app/

# Run the Django server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]