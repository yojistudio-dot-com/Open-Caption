# Use official lightweight Python 3.10 image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true

# Install system dependencies (FFmpeg for video subtitle burning, soundfile libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Upgrade pip and copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app

# Create cache directory for Whisper models to enable volume mounting
RUN mkdir -p /root/.cache/whisper

# Expose Streamlit default port
EXPOSE 8501

# Healthcheck to verify Streamlit service status
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch application
CMD ["streamlit", "run", "app.py"]
