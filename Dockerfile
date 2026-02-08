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

# --- NEW: DevOps Optimization ---
# Ensures logs appear in real-time in Docker/GitHub Actions
ENV PYTHONUNBUFFERED=1 
ENV PYTHONPATH=/app

COPY . .

# --- NEW: Infrastructure Proof ---
# Checks if the watcher process is actually alive every 30s
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD pgrep -f "python src/watcher.py" || exit 1

# --- UPDATED: Launch the Service ---
# Swapped from processor.py to watcher.py
CMD ["python", "src/watcher.py"]