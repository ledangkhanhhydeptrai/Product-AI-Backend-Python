FROM python:3.10-slim

WORKDIR /app

# system deps (QUAN TRỌNG cho torch + psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# upgrade pip
RUN pip install --upgrade pip setuptools wheel

# copy requirements trước để cache layer
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy source
COPY . .

# expose port
EXPOSE 8000

# run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]