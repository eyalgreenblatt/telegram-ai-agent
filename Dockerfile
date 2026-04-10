# ── Stage 1: builder ──────────────────────────────────────────────────────────
# Full image with build tools, compilers, and CUDA headers needed to compile
# torch, whisper, scipy, etc.  Nothing from this stage leaks into the final image.
FROM python:3.11 AS builder

# Install OS-level build dependencies (ffmpeg for pydub/whisper audio conversion)
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        build-essential \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy requirements first so Docker can cache the pip install layer
COPY requirements.txt .

# Install all Python dependencies into an isolated prefix so we can copy them
# cleanly into the runtime stage.  --no-cache-dir keeps this layer smaller.
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: runtime ──────────────────────────────────────────────────────────
# Slim base — no compilers, no build headers, no CUDA toolkit.
FROM python:3.11-slim AS runtime

# Runtime OS deps only: ffmpeg (required at runtime by pydub/whisper)
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy the pre-built Python packages from the builder stage
COPY --from=builder /install /usr/local

WORKDIR /app

# Copy application source
COPY . .

# Remove any leftover build artifacts and byte-code caches
RUN find /app -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true \
    && find /app -name "*.pyc" -delete 2>/dev/null || true

# Telegram bots are long-running workers, not HTTP servers
CMD ["python", "bot.py"]
