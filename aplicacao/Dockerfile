FROM python:3.9-slim

WORKDIR /app

# Install system dependencies FIRST (before pip install)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY templates/ templates/

# Create uploads directory
RUN mkdir -p uploads

EXPOSE 5000

CMD ["python", "app.py"]