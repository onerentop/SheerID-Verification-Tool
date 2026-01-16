# SheerID Verification Tool Docker Image
# Multi-stage build for smaller image size

# ============ Build Stage ============
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
COPY canva-teacher-tool/requirements.txt ./canva-requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --user \
    -r requirements.txt \
    -r canva-requirements.txt \
    curl_cffi \
    cloudscraper

# ============ Runtime Stage ============
FROM python:3.11-slim

LABEL maintainer="ThanhNguyxn"
LABEL description="SheerID Verification Tool - Multi-platform student/teacher/military verification"
LABEL version="1.0"

WORKDIR /app

# Install runtime dependencies (fonts for Pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core \
    fonts-liberation \
    fontconfig \
    && rm -rf /var/lib/apt/lists/* \
    && fc-cache -f -v

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY anti_detect.py .
COPY spotify-verify-tool ./spotify-verify-tool/
COPY youtube-verify-tool ./youtube-verify-tool/
COPY one-verify-tool ./one-verify-tool/
COPY boltnew-verify-tool ./boltnew-verify-tool/
COPY k12-verify-tool ./k12-verify-tool/
COPY veterans-verify-tool ./veterans-verify-tool/
COPY perplexity-verify-tool ./perplexity-verify-tool/
COPY canva-teacher-tool ./canva-teacher-tool/
COPY entrypoint.sh .

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Create non-root user for security
RUN useradd -m -s /bin/bash verifier \
    && chown -R verifier:verifier /app
USER verifier

# Default environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TOOL=one

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; import PIL; print('OK')" || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["--help"]
