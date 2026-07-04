# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Tắt cache python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cài dependencies hệ thống (quan trọng cho psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements trước để tối ưu cache
COPY requirements.txt .

# Cài python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Render sẽ set PORT, nhưng default fallback
ENV PORT=10000

# Mở port
EXPOSE 10000

# Start app (FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]