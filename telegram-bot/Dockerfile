# SheerID Telegram Bot Dockerfile
FROM python:3.11-slim

LABEL maintainer="ThanhNguyxn"
LABEL description="SheerID Verification Telegram Bot"
LABEL version="1.0"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    fonts-dejavu-core \
    fonts-liberation \
    fontconfig \
    && rm -rf /var/lib/apt/lists/* \
    && fc-cache -f -v

# Copy requirements first for caching
COPY telegram-bot/requirements.txt ./telegram-bot/
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir \
    -r requirements.txt \
    -r telegram-bot/requirements.txt

# Copy application code
COPY anti_detect.py .
COPY telegram-bot ./telegram-bot/
COPY spotify-verify-tool ./spotify-verify-tool/
COPY youtube-verify-tool ./youtube-verify-tool/
COPY one-verify-tool ./one-verify-tool/
COPY boltnew-verify-tool ./boltnew-verify-tool/
COPY k12-verify-tool ./k12-verify-tool/
COPY veterans-verify-tool ./veterans-verify-tool/
COPY perplexity-verify-tool ./perplexity-verify-tool/
COPY canva-teacher-tool ./canva-teacher-tool/

# Create data directory for stats persistence
RUN mkdir -p /app/data

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import telegram; import httpx; print('OK')" || exit 1

WORKDIR /app/telegram-bot

CMD ["python", "main.py"]
