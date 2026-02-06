FROM python:3.11-slim-bookworm

WORKDIR /app

# Upgrade system packages to catch the glibc fix
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Force upgrade pip, setuptools, and wheel before installing requirements
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
CMD ["sh", "-c", "python src/processor.py && pytest"]